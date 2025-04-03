import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';

const API_URL = import.meta.env.VITE_API_URL || '/api';

// Contact model definition
export interface Contact {
  id: string;
  name: string;
  client: string;
}

export interface ContactsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Contact[];
}

export interface ContactListParams {
  search?: string;
  ordering?: string;
  client?: string;
}

export const contactService = {
  async getContacts(params: ContactListParams = {}): Promise<ContactsResponse> {
    try {
      const apiParams = convertObjectKeysToSnake(params);
      const response = await axios.get(`${API_URL}/client/contacts/`, { params: apiParams });
      
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((contact: any) => convertObjectKeysToCamel(contact))
      };
    } catch (error: any) {
      console.error('Error fetching contacts:', error);
      throw error;
    }
  },

  async getContactById(id: string): Promise<Contact> {
    try {
      const response = await axios.get(`${API_URL}/client/contacts/${id}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error(`Error fetching contact with ID ${id}:`, error);
      throw error;
    }
  },

  async createContact(contactData: Partial<Contact>): Promise<Contact> {
    try {
      const apiData = convertObjectKeysToSnake(contactData);
      const response = await axios.post(`${API_URL}/client/contacts/`, apiData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error creating contact:', error);
      throw error;
    }
  },

  async updateContact(id: string, data: Partial<Contact>): Promise<Contact> {
    try {
      const apiData = convertObjectKeysToSnake(data);
      const response = await axios.patch(`${API_URL}/client/contacts/${id}/`, apiData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating contact:', error);
      throw error;
    }
  },

  async deleteContact(id: string): Promise<void> {
    try {
      await axios.delete(`${API_URL}/client/contacts/${id}/`);
    } catch (error: any) {
      console.error('Error deleting contact:', error);
      throw error;
    }
  }
}; 