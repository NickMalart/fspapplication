<template>
    <div class="address-autocomplete-container">
      <label :for="id" class="block text-sm font-medium text-gray-700">{{ label }}</label>
      <div class="relative">
        <input
          :id="id"
          v-model="searchInput"
          type="text"
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          :placeholder="placeholder"
          @input="onInput"
          @focus="onFocus"
          @blur="onBlur"
        />
        
        <div v-if="suggestions.length > 0 && showSuggestions" 
             class="absolute z-[99999] w-full mt-1 bg-white rounded-md shadow-lg border">
          <ul class="max-h-60 overflow-auto">
            <li v-for="suggestion in suggestions" 
                :key="suggestion.placeId" 
                class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectAddress(suggestion)"
                @click="selectAddress(suggestion)">
              {{ suggestion.description }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, watch } from 'vue';
  import axios from 'axios';
  import { debounce } from 'lodash';
  
  interface Suggestion {
    placeId: string;
    description: string;
  }
  
  interface AddressComponents {
    street_number?: string;
    route?: string;
    locality?: string;
    administrative_area_level_1?: string;
    country?: string;
    postal_code?: string;
    sublocality?: string;
    [key: string]: string | undefined;
  }
  
  export default defineComponent({
    name: 'AddressAutocomplete',
    props: {
      modelValue: {
        type: Object,
        default: () => ({})
      },
      label: {
        type: String,
        default: 'Address'
      },
      placeholder: {
        type: String,
        default: 'Start typing to search for an address'
      },
      id: {
        type: String,
        default: 'address-autocomplete'
      }
    },
    emits: ['update:modelValue'],
    setup(props, { emit }) {
      const searchInput = ref('');
      const suggestions = ref<Suggestion[]>([]);
      const showSuggestions = ref(false);
      
      // Create a debounced function for API calls
      const fetchSuggestions = debounce(async (input: string) => {
        if (!input || input.length < 3) {
          suggestions.value = [];
          return;
        }
        
        try {
          console.log('Fetching suggestions for:', input);
          const response = await axios.get('/api/places/autocomplete/', {
            params: { input }
          });
          
          console.log('Autocomplete API response:', response.data);
          if (response.data.predictions) {
            suggestions.value = response.data.predictions;
            console.log('Suggestions loaded:', suggestions.value);
          }
        } catch (error) {
          console.error('Error fetching address suggestions:', error);
          suggestions.value = [];
        }
      }, 300);
      
      const onInput = () => {
        fetchSuggestions(searchInput.value);
      };
      
      const onFocus = () => {
        showSuggestions.value = true;
      };
      
      const onBlur = () => {
        // Delay hiding suggestions to allow click on suggestion
        setTimeout(() => {
          showSuggestions.value = false;
        }, 300);
      };
      
      const selectAddress = async (suggestion: Suggestion) => {
        try {
          console.log('Selected suggestion:', suggestion);
          
          if (!suggestion || !suggestion.placeId) {
            console.error('No placeId found in suggestion:', suggestion);
            return;
          }
          
          console.log('Fetching place details for placeId:', suggestion.placeId);
          const response = await axios.get('/api/places/details/', {
            params: { place_id: suggestion.placeId }
          });
          
          console.log('Place details response:', response.data);
          console.log('Response status:', response.data.status);
          
          if (response.data.result) {
            const result = response.data.result;
            console.log('Result structure:', Object.keys(result));
            console.log('Full result:', result);
            const formattedAddress = result.formatted_address || result.formattedAddress || '';
            console.log('Formatted address:', formattedAddress);
            
            // Parse address components
            const addressComponents: AddressComponents = {};
            
            // Check for both snake_case and camelCase properties
            const components = result.address_components || result.addressComponents;
            
            // Add null check for address_components
            if (components && Array.isArray(components)) {
              console.log('Address components:', components);
              
              components.forEach((component: any) => {
                const types = component.types;
                console.log('Component types:', types, 'value:', component.long_name);
                
                if (types && Array.isArray(types)) {
                  if (types.includes('street_number')) {
                    addressComponents.street_number = component.long_name;
                  } else if (types.includes('route')) {
                    addressComponents.route = component.long_name;
                  } else if (types.includes('locality')) {
                    addressComponents.locality = component.long_name;
                  } else if (types.includes('administrative_area_level_1')) {
                    addressComponents.administrative_area_level_1 = component.short_name;
                  } else if (types.includes('country')) {
                    addressComponents.country = component.long_name;
                  } else if (types.includes('postal_code')) {
                    addressComponents.postal_code = component.long_name;
                  } else if (types.includes('sublocality')) {
                    // Add support for suburb/sublocality
                    addressComponents.sublocality = component.long_name;
                  }
                }
              });
              
              console.log('Parsed address components:', addressComponents);
            } else {
              console.warn('No address_components in result:', result);
            }
            
            // Extract individual parts from the formatted address if components are empty
            let street = '';
            let city = '';
            let state = '';
            let country = '';
            let postal_code = '';
            
            // First try to get data from the address components
            if (addressComponents.street_number && addressComponents.route) {
              street = `${addressComponents.street_number} ${addressComponents.route}`;
            }
            
            city = addressComponents.locality || addressComponents.sublocality || '';
            state = addressComponents.administrative_area_level_1 || '';
            country = addressComponents.country || '';
            postal_code = addressComponents.postal_code || '';
            
            // If any fields are missing, try to parse from the formatted address
            if ((!street || !city || !state || !postal_code || !country) && formattedAddress) {
              // Example: "8 Park Ave, Nirimba QLD 4551, Australia"
              const parts = formattedAddress.split(',').map((part: string) => part.trim());
              console.log('Address parts:', parts);
              
              // First part is usually the street
              if (!street && parts.length > 0) {
                street = parts[0];
              }
              
              // Process the remaining parts
              if (parts.length > 1) {
                // Second part often contains suburb/city and sometimes state
                const secondPart = parts[1];
                
                if (!city && secondPart) {
                  // Try to extract city and state from second part
                  // Example: "Nirimba QLD" -> ["Nirimba", "QLD"]
                  const cityStateParts = secondPart.trim().split(' ');
                  
                  if (cityStateParts.length > 1) {
                    // Last part is likely the state
                    const possibleState = cityStateParts[cityStateParts.length - 1];
                    
                    // Check if it looks like a state code (2-3 uppercase letters)
                    if (possibleState.length <= 3 && possibleState === possibleState.toUpperCase()) {
                      if (!state) state = possibleState;
                      
                      // City is everything before the state
                      if (!city) city = cityStateParts.slice(0, -1).join(' ');
                    } else {
                      // The whole thing is probably the city
                      if (!city) city = secondPart;
                    }
                  } else {
                    // Just one word, assume it's the city
                    if (!city) city = secondPart;
                  }
                }
              }
              
              // Third part often contains postal code and maybe state
              if (parts.length > 2) {
                const thirdPart = parts[2].trim();
                
                // Try to extract postal code
                const postalCodeMatch = thirdPart.match(/\d+/);
                if (!postal_code && postalCodeMatch) {
                  postal_code = postalCodeMatch[0];
                }
                
                // If state is still empty, check if there's a state code in this part
                if (!state) {
                  const thirdPartWords = thirdPart.split(' ');
                  for (const word of thirdPartWords) {
                    if (word.length <= 3 && word === word.toUpperCase() && !/\d/.test(word)) {
                      state = word;
                      break;
                    }
                  }
                }
              }
              
              // Last part is usually the country
              if (!country && parts.length > 3) {
                country = parts[parts.length - 1];
              } else if (!country && parts.length > 2) {
                // If we only have 3 parts, the last one might be the country
                const lastPart = parts[parts.length - 1].trim();
                // Only use it as country if it doesn't contain numbers (to avoid using postal code as country)
                if (!/\d/.test(lastPart)) {
                  country = lastPart;
                }
              }
            }
            
            console.log('Extracted address parts:', { street, city, state, postal_code, country });
            
            // Get coordinates from either naming convention
            const location = result.geometry?.location || {};
            const lat = location.lat || null;
            const lng = location.lng || null;
            
            // Build complete address data
            const addressData = {
              formatted_address: formattedAddress,
              components: addressComponents,
              street: street,
              city: city,
              state: state,
              country: country,
              postal_code: postal_code,
              lat: lat,
              lng: lng,
              place_id: suggestion.placeId
            };
            
            console.log('Final address data to emit:', addressData);
            
            // Update the model value
            emit('update:modelValue', addressData);
            
            // Update input field with formatted address
            searchInput.value = formattedAddress;
            
            // Clear suggestions
            suggestions.value = [];
          }
        } catch (error) {
          console.error('Error fetching address details:', error);
        }
      };
      
      // Update input field when model changes externally
      watch(() => props.modelValue, (newValue) => {
        if (newValue && newValue.formatted_address) {
          searchInput.value = newValue.formatted_address;
        }
      }, { immediate: true });
      
      return {
        searchInput,
        suggestions,
        showSuggestions,
        onInput,
        onFocus,
        onBlur,
        selectAddress
      };
    }
  });
  </script>