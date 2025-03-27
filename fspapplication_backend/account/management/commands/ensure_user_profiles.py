from django.core.management.base import BaseCommand
from account.models import User, UserProfile


class Command(BaseCommand):
    help = "Ensures all users have a UserProfile"

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile=None)
        profile_count = 0
        
        if not users_without_profiles.exists():
            self.stdout.write(self.style.SUCCESS("All users already have profiles!"))
            return
            
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            profile_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f"Created {profile_count} user profiles successfully!")
        ) 