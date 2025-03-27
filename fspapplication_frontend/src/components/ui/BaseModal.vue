<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue';

export default defineComponent({
  name: 'BaseModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    maxWidth: {
      type: String,
      default: 'max-w-[700px]'
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const closeModal = () => {
      emit('update:modelValue', false);
    };

    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        closeModal();
      }
    };

    onMounted(() => {
      document.addEventListener('keydown', handleEscKey);
    });

    onUnmounted(() => {
      document.removeEventListener('keydown', handleEscKey);
    });

    return {
      closeModal
    };
  }
});
</script>

<template>
  <teleport to="body">
    <div
      v-if="modelValue"
      class="fixed inset-0 flex items-center justify-center p-5 overflow-y-auto z-50"
    >
      <div
        class="modal-backdrop fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
        @click="closeModal"
      ></div>
      <div
        class="no-scrollbar relative flex w-full flex-col overflow-y-auto rounded-3xl bg-white p-6 dark:bg-gray-900 lg:p-11"
        :class="maxWidth"
        @click.stop
      >
        <!-- close btn -->
        <button
          @click="closeModal"
          class="transition-color absolute right-5 top-5 z-10 flex h-11 w-11 items-center justify-center rounded-full bg-gray-100 text-gray-400 hover:bg-gray-200 hover:text-gray-600 dark:bg-gray-700 dark:bg-white/[0.05] dark:text-gray-400 dark:hover:bg-white/[0.07] dark:hover:text-gray-300"
        >
          <svg
            class="fill-current"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M6.04289 16.5418C5.65237 16.9323 5.65237 17.5655 6.04289 17.956C6.43342 18.3465 7.06658 18.3465 7.45711 17.956L11.9987 13.4144L16.5408 17.9565C16.9313 18.347 17.5645 18.347 17.955 17.9565C18.3455 17.566 18.3455 16.9328 17.955 16.5423L13.4129 12.0002L17.955 7.45808C18.3455 7.06756 18.3455 6.43439 17.955 6.04387C17.5645 5.65335 16.9313 5.65335 16.5408 6.04387L11.9987 10.586L7.45711 6.04439C7.06658 5.65386 6.43342 5.65386 6.04289 6.04439C5.65237 6.43491 5.65237 7.06808 6.04289 7.4586L10.5845 12.0002L6.04289 16.5418Z"
              fill=""
            />
          </svg>
        </button>

        <div v-if="title || description" class="px-2 pr-14">
          <h4 v-if="title" class="mb-2 text-2xl font-semibold text-gray-800 dark:text-white/90">
            {{ title }}
          </h4>
          <p v-if="description" class="mb-6 text-sm text-gray-500 dark:text-gray-400 lg:mb-7">
            {{ description }}
          </p>
        </div>

        <div class="flex flex-col flex-grow">
          <slot></slot>
        </div>

        <div v-if="$slots.footer" class="flex items-center gap-3 mt-6 lg:justify-end">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </teleport>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style> 