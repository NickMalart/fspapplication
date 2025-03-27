# Singleton Form Save Implementation Guide

## What is a Singleton Pattern?
- Ensures only one instance of a model exists in the database
- Useful for company settings, global configurations, or organization details
- Prevents duplicate entries for unique system-wide settings

## Implementation Steps with Examples

### 1. Django Backend Setup

#### Step 1.1: Create the Model
```python
# myapp/models.py
from django.db import models
from django.core.exceptions import ValidationError

class SingletonModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    settings_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Ensure only one instance exists"""
        if not self.pk and SingletonModel.objects.exists():
            raise ValidationError('Only one instance allowed')
        return super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Get or create the single instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
```

#### Step 1.2: Create the Serializer
```python
# myapp/serializers.py
from rest_framework import serializers
from .models import SingletonModel

class SingletonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingletonModel
        fields = ['name', 'email', 'settings_json']
```

#### Step 1.3: Create the ViewSet
```python
# myapp/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SingletonModel
from .serializers import SingletonSerializer

class SingletonViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        instance = SingletonModel.get_solo()
        serializer = SingletonSerializer(instance)
        return Response(serializer.data)

    def update(self, request):
        instance = SingletonModel.get_solo()
        serializer = SingletonSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### Step 1.4: Configure URLs
```python
# myapp/urls.py
from django.urls import path
from .views import SingletonViewSet

urlpatterns = [
    path('settings/', SingletonViewSet.as_view({
        'get': 'retrieve',
        'put': 'update'
    }), name='settings'),
]

# project/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.urls')),
]
```

### 2. Frontend Setup

#### Step 2.1: Create the Store (Pinia)
```typescript
// stores/settings.ts
import { defineStore } from 'pinia'
import axios from 'axios'

interface Settings {
  name: string
  email: string
  settings_json: Record<string, any>
}

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: null as Settings | null,
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchSettings() {
      this.loading = true
      try {
        const response = await axios.get('/api/settings/')
        this.settings = response.data
      } catch (error) {
        this.error = 'Failed to fetch settings'
      } finally {
        this.loading = false
      }
    },

    async updateSettings(data: Partial<Settings>) {
      this.loading = true
      try {
        const response = await axios.put('/api/settings/', data)
        this.settings = response.data
        return true
      } catch (error) {
        this.error = 'Failed to update settings'
        return false
      } finally {
        this.loading = false
      }
    }
  }
})
```

#### Step 2.2: Create the Form Component
```vue
<!-- components/SettingsForm.vue -->
<template>
  <form @submit.prevent="saveSettings" class="space-y-4">
    <div>
      <label>Name</label>
      <input 
        v-model="formData.name" 
        type="text" 
        class="form-input"
      />
    </div>

    <div>
      <label>Email</label>
      <input 
        v-model="formData.email" 
        type="email" 
        class="form-input"
      />
    </div>

    <div class="flex justify-end">
      <button 
        type="submit" 
        :disabled="loading"
        class="btn-primary"
      >
        {{ loading ? 'Saving...' : 'Save Changes' }}
      </button>
    </div>

    <div v-if="error" class="text-red-500">
      {{ error }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useSettingsStore } from '@/stores/settings'

const store = useSettingsStore()
const loading = computed(() => store.loading)
const error = computed(() => store.error)

const formData = ref({
  name: '',
  email: ''
})

async function saveSettings() {
  const success = await store.updateSettings(formData.value)
  if (success) {
    // Handle success (e.g., show notification)
  }
}

// Initialize form with current settings
onMounted(async () => {
  await store.fetchSettings()
  if (store.settings) {
    formData.value = { ...store.settings }
  }
})
</script>
```
### 1. Django Backend Setup

#### Step 1.1: Create the Model
- Create a Django model with your required fields
- Add a custom save method to prevent multiple instances
- Implement a `get_solo()` method to always retrieve the same instance
- Define necessary fields (e.g., company name, settings, configurations)

#### Step 1.2: Create the Serializer
- Create a Django REST Framework serializer
- Define which fields should be exposed to the API
- Add any validation rules
- Handle special fields (like file uploads) if needed

#### Step 1.3: Create the ViewSet
- Implement a ViewSet with retrieve (GET) and update (PUT) methods
- Use `get_solo()` to always work with the same instance
- Handle validation and responses
- Implement error handling

#### Step 1.4: Configure URLs
- Set up URL patterns for your API endpoints
- Include them in your main URL configuration
- Ensure proper URL naming and structure

### 2. Frontend Setup

#### Step 2.1: Create the Store
- Set up a Pinia store (or Vuex if preferred)
- Define the state structure
- Implement actions for API communication
- Handle loading and error states

#### Step 2.2: Define Types (TypeScript)
- Create interfaces for your data structures
- Define store types
- Set up API response types
- Ensure type safety across your application

#### Step 2.3: Create the Form Component
- Build the form interface
- Implement data binding
- Handle form submission
- Show loading and error states
- Display success/failure messages

1. **User Input**
   - User enters data into the form
   - Form component manages local state

2. **Form Submission**
   - Validate form data
   - Prepare data for API submission
   - Show loading state

3. **Store Action**
   - Call store action with form data
   - Make API request
   - Handle response

4. **API Processing**
   - Backend receives request
   - Validates data
   - Updates single instance
   - Returns response

5. **Response Handling**
   - Update store state
   - Show success/error message
   - Reset form if needed
   - Update UI

### 4. Best Practices

#### Backend
- Always validate data thoroughly
- Use transactions where necessary
- Implement proper error handling
- Add appropriate permissions
- Document your API endpoints

#### Frontend
- Implement proper form validation
- Show clear loading states
- Handle errors gracefully
- Use TypeScript for better type safety
- Keep store actions focused

### 5. Testing

#### Backend Tests
- Test model singleton behavior
- Verify API endpoints
- Check validation rules
- Test error cases

#### Frontend Tests
- Test form submission
- Verify store actions
- Check error handling
- Test loading states

## Common Pitfalls to Avoid
1. Not handling race conditions
2. Missing error cases
3. Insufficient validation
4. Poor user feedback
5. Not considering offline scenarios

## Security Considerations
1. Implement proper authentication
2. Add necessary permissions
3. Validate data on both ends
4. Sanitize user input
5. Handle sensitive data appropriately

## Performance Tips
1. Optimize database queries
2. Implement caching where appropriate
3. Minimize API calls
4. Handle large datasets efficiently
5. Consider debouncing/throttling