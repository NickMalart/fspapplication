import { ref } from 'vue';

type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
  id: number;
  message: string;
  type: ToastType;
  timeout: number;
}

const toasts = ref<Toast[]>([]);
let nextId = 1;

export function useToast() {
  const showToast = (message: string, type: ToastType = 'info', timeout: number = 3000) => {
    const id = nextId++;
    const toast: Toast = {
      id,
      message,
      type,
      timeout,
    };
    
    toasts.value.push(toast);
    
    // Auto-remove toast after timeout
    setTimeout(() => {
      removeToast(id);
    }, timeout);
    
    return id;
  };
  
  const removeToast = (id: number) => {
    const index = toasts.value.findIndex(t => t.id === id);
    if (index !== -1) {
      toasts.value.splice(index, 1);
    }
  };
  
  return {
    toasts,
    showToast,
    removeToast,
  };
} 