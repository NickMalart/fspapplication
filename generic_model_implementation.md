# Generic Model Implementation Guide (Django-Tenants to Vue.js)

## 1. Backend Implementation (Django)

### 1.1 Model Creation
```python
# app/models.py
from django.db import models

class GenericModel(models.Model):
    # Common fields that most models might have
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Make this an abstract base class

    def __str__(self):
        return self.name
```

### 1.2 Serializer Template
```python
# app/serializers.py
from rest_framework import serializers

class GenericModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Replace with your actual model
        fields = '__all__'  # Or specify fields: ['id', 'name', 'description', ...]
        read_only_fields = ['created_at', 'updated_at']
```

### 1.3 ViewSet Template
```python
# app/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class GenericModelViewSet(viewsets.ModelViewSet):
    serializer_class = None  # Replace with your serializer
    queryset = None  # Replace with your model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Add any custom filtering here
        return super().get_queryset()
```

### 1.4 URLs Configuration
```python
# app/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('your-model', GenericModelViewSet, basename='your-model')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## 2. Frontend Implementation (Vue.js + TypeScript)

### 2.1 Types Definition
```typescript
// types/models.ts
export interface GenericModel {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
```

### 2.2 API Service
```typescript
// services/api.ts
import axios from 'axios';
import { GenericModel } from '@/types/models';

export class GenericApiService {
  private baseUrl: string;

  constructor(endpoint: string) {
    this.baseUrl = `/api/${endpoint}`;
  }

  async getAll(): Promise<GenericModel[]> {
    const response = await axios.get(this.baseUrl);
    return response.data;
  }

  async getById(id: number): Promise<GenericModel> {
    const response = await axios.get(`${this.baseUrl}/${id}`);
    return response.data;
  }

  async create(data: Partial<GenericModel>): Promise<GenericModel> {
    const response = await axios.post(this.baseUrl, data);
    return response.data;
  }

  async update(id: number, data: Partial<GenericModel>): Promise<GenericModel> {
    const response = await axios.put(`${this.baseUrl}/${id}`, data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await axios.delete(`${this.baseUrl}/${id}`);
  }
}
```

### 2.3 Vue Store Module (Pinia)
```typescript
// stores/genericStore.ts
import { defineStore } from 'pinia';
import { GenericModel } from '@/types/models';
import { GenericApiService } from '@/services/api';

export const useGenericStore = defineStore('generic', {
  state: () => ({
    items: [] as GenericModel[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchAll() {
      this.loading = true;
      try {
        const api = new GenericApiService('your-endpoint');
        this.items = await api.getAll();
      } catch (err) {
        this.error = 'Failed to fetch items';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async createItem(data: Partial<GenericModel>) {
      const api = new GenericApiService('your-endpoint');
      const newItem = await api.create(data);
      this.items.push(newItem);
    },

    async updateItem(id: number, data: Partial<GenericModel>) {
      const api = new GenericApiService('your-endpoint');
      const updated = await api.update(id, data);
      const index = this.items.findIndex(item => item.id === id);
      if (index !== -1) {
        this.items[index] = updated;
      }
    },

    async deleteItem(id: number) {
      const api = new GenericApiService('your-endpoint');
      await api.delete(id);
      this.items = this.items.filter(item => item.id !== id);
    },
  },
});
```

### 2.4 Vue Component Template
```vue
<!-- components/GenericList.vue -->
<template>
  <div class="container mx-auto p-4">
    <!-- List View -->
    <div class="bg-white shadow-md rounded-lg">
      <div class="flex justify-between items-center p-4 border-b">
        <h2 class="text-xl font-semibold">Items List</h2>
        <button
          @click="showCreateModal = true"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Add New
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="store.loading" class="p-4">
        <p class="text-gray-500">Loading...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="store.error" class="p-4 text-red-500">
        {{ store.error }}
      </div>

      <!-- Data Table -->
      <table v-else class="min-w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Description
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in store.items" :key="item.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ item.name }}</td>
            <td class="px-6 py-4">{{ item.description }}</td>
            <td class="px-6 py-4">
              <span
                :class="item.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
              >
                {{ item.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <button
                @click="editItem(item)"
                class="text-indigo-600 hover:text-indigo-900 mr-2"
              >
                Edit
              </button>
              <button
                @click="deleteItem(item.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useGenericStore } from '@/stores/genericStore';

const store = useGenericStore();
const showCreateModal = ref(false);

onMounted(async () => {
  await store.fetchAll();
});

const editItem = (item: GenericModel) => {
  // Implement edit logic
};

const deleteItem = async (id: number) => {
  if (confirm('Are you sure you want to delete this item?')) {
    await store.deleteItem(id);
  }
};
</script>
```

## 3. Implementation Steps

1. **Backend Setup**:
   - Create your model by extending the GenericModel class
   - Create a serializer extending GenericModelSerializer
   - Create a ViewSet extending GenericModelViewSet
   - Add URLs to your router

2. **Frontend Setup**:
   - Create model interface extending GenericModel
   - Create API service instance
   - Create Pinia store
   - Create Vue components for list/detail views

## 4. Best Practices

1. **Error Handling**:
   - Implement proper error handling in both backend and frontend
   - Use try-catch blocks for async operations
   - Display user-friendly error messages

2. **Authentication**:
   - Ensure proper authentication headers are set
   - Implement permission checks in ViewSets
   - Handle token refresh on the frontend

3. **Data Validation**:
   - Use Django model validators
   - Implement frontend form validation
   - Sanitize user inputs

4. **Performance**:
   - Use pagination for large datasets
   - Implement caching where appropriate
   - Optimize database queries

5. **Security**:
   - Use CSRF tokens
   - Implement rate limiting
   - Validate file uploads
   - Sanitize user inputs

## 5. Testing

1. **Backend Tests**:
   - Model tests
   - API endpoint tests
   - Serializer tests

2. **Frontend Tests**:
   - Component tests
   - Store tests
   - API service tests

This template provides a foundation that can be customized for any model in your application while maintaining consistent patterns and best practices. 