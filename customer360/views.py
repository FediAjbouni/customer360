from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from django.db.models import Count
import logging
from customer_management.models import Customer
from interactions.models import Interaction

logger = logging.getLogger(__name__)

def index(request):
    """
    Display all customers in a table format.
    """
    try:
        customers = Customer.objects.all().order_by('name')
        logger.info(f"Retrieved {customers.count()} customers for display")
        context = {"customers": customers}
        return render(request, "index.html", context=context)
    except Exception as e:
        logger.error(f"Error retrieving customers: {str(e)}")
        messages.error(request, "An error occurred while loading customers.")
        return render(request, "index.html", {"customers": []})

def create_customer(request):
    """
    Create a new customer with proper validation and error handling.
    """
    if request.method == "POST":
        try:
            # Get and validate form data
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            social_media = request.POST.get("social_media", "").strip()
            
            # Basic validation
            if not all([name, email, phone, address]):
                messages.error(request, "All required fields must be filled.")
                return render(request, "add.html")
            
            # Check for duplicate email
            if Customer.objects.filter(email=email).exists():
                messages.error(request, "A customer with this email already exists.")
                return render(request, "add.html")
            
            # Create customer
            customer = Customer.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                social_media=social_media
            )
            
            logger.info(f"Created new customer: {customer.name} (ID: {customer.id})")
            messages.success(request, f"Successfully created customer: {customer.name}")
            return redirect('index')
            
        except ValidationError as e:
            logger.warning(f"Validation error creating customer: {str(e)}")
            messages.error(request, f"Validation error: {str(e)}")
        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            messages.error(request, "A customer with this information already exists.")
        except Exception as e:
            logger.error(f"Unexpected error creating customer: {str(e)}")
            messages.error(request, "An unexpected error occurred. Please try again.")
    
    return render(request, "add.html")


def summary(request):
    """
    Display interaction summary for the last 30 days with proper error handling.
    """
    try:
        thirty_days_ago = date.today() - timedelta(days=30)
        interactions_queryset = Interaction.objects.filter(interaction_date__gte=thirty_days_ago)
        
        count = interactions_queryset.count()
        interactions = interactions_queryset.values("channel", "direction").annotate(count=Count('channel'))
        
        logger.info(f"Generated summary for {count} interactions in last 30 days")
        
        context = {
            "interactions": interactions,
            "count": count,
            "date_range": f"{thirty_days_ago.strftime('%Y-%m-%d')} to {date.today().strftime('%Y-%m-%d')}"
        }
        
        return render(request, "summary.html", context=context)
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        messages.error(request, "An error occurred while generating the summary.")
        return render(request, "summary.html", {"interactions": [], "count": 0})

def interact(request, cid):
    """
    Handle customer interactions with proper validation and error handling.
    """
    try:
        customer = get_object_or_404(Customer, id=cid)
        channels = Interaction.CHANNEL_CHOICES
        directions = Interaction.DIRECTION_CHOICES
        
        context = {
            "channels": channels,
            "directions": directions,
            "customer": customer
        }

        if request.method == "POST":
            try:
                channel = request.POST.get("channel")
                direction = request.POST.get("direction")
                summary = request.POST.get("summary", "").strip()
                
                # Validation
                if not all([channel, direction, summary]):
                    messages.error(request, "All fields are required.")
                    return render(request, "interact.html", context=context)
                
                if channel not in dict(Interaction.CHANNEL_CHOICES):
                    messages.error(request, "Invalid channel selected.")
                    return render(request, "interact.html", context=context)
                
                if direction not in dict(Interaction.DIRECTION_CHOICES):
                    messages.error(request, "Invalid direction selected.")
                    return render(request, "interact.html", context=context)
                
                # Create interaction
                interaction = Interaction.objects.create(
                    customer=customer,
                    channel=channel,
                    direction=direction,
                    summary=summary
                )
                
                logger.info(f"Created interaction for customer {customer.name} (ID: {customer.id})")
                messages.success(request, "Interaction recorded successfully!")
                return redirect('index')
                
            except ValidationError as e:
                logger.warning(f"Validation error in interaction: {str(e)}")
                messages.error(request, f"Validation error: {str(e)}")
            except Exception as e:
                logger.error(f"Error creating interaction: {str(e)}")
                messages.error(request, "An error occurred while saving the interaction.")

        return render(request, "interact.html", context=context)
        
    except Exception as e:
        logger.error(f"Error in interact view: {str(e)}")
        messages.error(request, "Customer not found or an error occurred.")
        return redirect('index')