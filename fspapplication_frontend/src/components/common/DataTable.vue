<template>
  <!-- Outer container matching the original structure -->
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    <div class="px-5 py-4 sm:px-6 sm:py-5">
      <h3 class="text-base font-medium text-gray-800 dark:text-white/90">
        User Accounts
      </h3>
    </div>
    <div class="border-t border-gray-100 p-5 dark:border-gray-800 sm:p-6">
      <!-- DataTable Component Start -->
      <div class="overflow-hidden rounded-xl border border-gray-200 bg-white pt-4 dark:border-gray-800 dark:bg-white/[0.03]">
        <!-- Controls: Show Entries & Search -->
        <div class="mb-4 flex flex-col gap-2 px-4 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-3">
            <span class="text-gray-500 dark:text-gray-400"> Show </span>
            <div class="relative z-20 bg-transparent">
              <!-- Use v-model for two-way binding with perPage -->
              <select
                v-model.number="perPage"
                class="dark:bg-dark-900 h-9 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none py-2 pl-3 pr-8 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              >
                <option value="10" class="text-gray-500 dark:bg-gray-900 dark:text-gray-400">10</option>
                <option value="8" class="text-gray-500 dark:bg-gray-900 dark:text-gray-400">8</option>
                <option value="5" class="text-gray-500 dark:bg-gray-900 dark:text-gray-400">5</option>
                <option value="20" class="text-gray-500 dark:bg-gray-900 dark:text-gray-400">20</option> <!-- Added another option -->
              </select>
              <span class="absolute right-2 top-1/2 z-30 -translate-y-1/2 text-gray-500 dark:text-gray-400">
                <svg class="stroke-current" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3.8335 5.9165L8.00016 10.0832L12.1668 5.9165" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </span>
            </div>
            <span class="text-gray-500 dark:text-gray-400"> entries </span>
          </div>

          <div class="relative">
            <button class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400">
              <svg class="fill-current" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M3.04199 9.37363C3.04199 5.87693 5.87735 3.04199 9.37533 3.04199C12.8733 3.04199 15.7087 5.87693 15.7087 9.37363C15.7087 12.8703 12.8733 15.7053 9.37533 15.7053C5.87735 15.7053 3.04199 12.8703 3.04199 9.37363ZM9.37533 1.54199C5.04926 1.54199 1.54199 5.04817 1.54199 9.37363C1.54199 13.6991 5.04926 17.2053 9.37533 17.2053C11.2676 17.2053 13.0032 16.5344 14.3572 15.4176L17.1773 18.238C17.4702 18.5309 17.945 18.5309 18.2379 18.238C18.5308 17.9451 18.5309 17.4703 18.238 17.1773L15.4182 14.3573C16.5367 13.0033 17.2087 11.2669 17.2087 9.37363C17.2087 5.04817 13.7014 1.54199 9.37533 1.54199Z" />
              </svg>
            </button>
            <!-- Use v-model for two-way binding with search -->
            <input
              type="text"
              v-model="search"
              placeholder="Search..."
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent py-2.5 pl-11 pr-4 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800 xl:w-[300px]"
            />
          </div>
        </div>

        <!-- Table -->
        <div class="max-w-full overflow-x-auto">
          <div class="min-w-[1102px]">
            <!-- Table Header -->
            <div class="grid grid-cols-12 border-t border-gray-200 dark:border-gray-800">
              <!-- User Column Header -->
              <div class="col-span-3 flex items-center border-r border-gray-200 px-4 py-3 dark:border-gray-800">
                <div class="flex w-full cursor-pointer items-center justify-between" @click="sortBy('name')">
                  <p class="text-theme-xs font-medium text-gray-700 dark:text-gray-400">User</p>
                  <span class="flex flex-col gap-0.5">
                    <!-- Add dynamic classes for sort indicators later if needed -->
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 0.585167C4.21057 0.300808 3.78943 0.300807 3.59038 0.585166L1.05071 4.21327C0.81874 4.54466 1.05582 5 1.46033 5H6.53967C6.94418 5 7.18126 4.54466 6.94929 4.21327L4.40962 0.585167Z"/></svg>
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 4.41483C4.21057 4.69919 3.78943 4.69919 3.59038 4.41483L1.05071 0.786732C0.81874 0.455343 1.05582 0 1.46033 0H6.53967C6.94418 0 7.18126 0.455342 6.94929 0.786731L4.40962 4.41483Z"/></svg>
                  </span>
                </div>
              </div>
              <!-- Position Column Header -->
              <div class="col-span-2 flex items-center border-r border-gray-200 px-4 py-3 dark:border-gray-800">
                 <div class="flex w-full cursor-pointer items-center justify-between" @click="sortBy('position')">
                  <p class="text-theme-xs font-medium text-gray-700 dark:text-gray-400">Position</p>
                  <span class="flex flex-col gap-0.5">
                     <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 0.585167C4.21057 0.300808 3.78943 0.300807 3.59038 0.585166L1.05071 4.21327C0.81874 4.54466 1.05582 5 1.46033 5H6.53967C6.94418 5 7.18126 4.54466 6.94929 4.21327L4.40962 0.585167Z"/></svg>
                     <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 4.41483C4.21057 4.69919 3.78943 4.69919 3.59038 4.41483L1.05071 0.786732C0.81874 0.455343 1.05582 0 1.46033 0H6.53967C6.94418 0 7.18126 0.455342 6.94929 0.786731L4.40962 4.41483Z"/></svg>
                  </span>
                </div>
              </div>
              <!-- Office Column Header -->
              <div class="col-span-2 flex items-center border-r border-gray-200 px-4 py-3 dark:border-gray-800">
                 <div class="flex w-full cursor-pointer items-center justify-between" @click="sortBy('office')">
                  <p class="text-theme-xs font-medium text-gray-700 dark:text-gray-400">Office</p>
                  <span class="flex flex-col gap-0.5">
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 0.585167C4.21057 0.300808 3.78943 0.300807 3.59038 0.585166L1.05071 4.21327C0.81874 4.54466 1.05582 5 1.46033 5H6.53967C6.94418 5 7.18126 4.54466 6.94929 4.21327L4.40962 0.585167Z"/></svg>
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 4.41483C4.21057 4.69919 3.78943 4.69919 3.59038 4.41483L1.05071 0.786732C0.81874 0.455343 1.05582 0 1.46033 0H6.53967C6.94418 0 7.18126 0.455342 6.94929 0.786731L4.40962 4.41483Z"/></svg>
                  </span>
                </div>
              </div>
              <!-- Age Column Header -->
              <div class="col-span-1 flex items-center border-r border-gray-200 px-4 py-3 dark:border-gray-800">
                 <div class="flex w-full cursor-pointer items-center justify-between" @click="sortBy('age')">
                  <p class="text-theme-xs font-medium text-gray-700 dark:text-gray-400">Age</p>
                  <span class="flex flex-col gap-0.5">
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 0.585167C4.21057 0.300808 3.78943 0.300807 3.59038 0.585166L1.05071 4.21327C0.81874 4.54466 1.05582 5 1.46033 5H6.53967C6.94418 5 7.18126 4.54466 6.94929 4.21327L4.40962 0.585167Z"/></svg>
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 4.41483C4.21057 4.69919 3.78943 4.69919 3.59038 4.41483L1.05071 0.786732C0.81874 0.455343 1.05582 0 1.46033 0H6.53967C6.94418 0 7.18126 0.455342 6.94929 0.786731L4.40962 4.41483Z"/></svg>
                  </span>
                </div>
              </div>
              <!-- Start Date Column Header -->
              <div class="col-span-2 flex items-center border-r border-gray-200 px-4 py-3 dark:border-gray-800">
                 <div class="flex w-full cursor-pointer items-center justify-between" @click="sortBy('startDate')">
                  <p class="text-theme-xs font-medium text-gray-700 dark:text-gray-400">Start date</p>
                   <span class="flex flex-col gap-0.5">
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 0.585167C4.21057 0.300808 3.78943 0.300807 3.59038 0.585166L1.05071 4.21327C0.81874 4.54466 1.05582 5 1.46033 5H6.53967C6.94418 5 7.18126 4.54466 6.94929 4.21327L4.40962 0.585167Z"/></svg>
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 4.41483C4.21057 4.69919 3.78943 4.69919 3.59038 4.41483L1.05071 0.786732C0.81874 0.455343 1.05582 0 1.46033 0H6.53967C6.94418 0 7.18126 0.455342 6.94929 0.786731L4.40962 4.41483Z"/></svg>
                  </span>
                </div>
              </div>
              <!-- Salary Column Header -->
              <div class="col-span-2 flex items-center px-4 py-3">
                 <div class="flex w-full cursor-pointer items-center justify-between" @click="sortBy('salary')">
                  <p class="text-theme-xs font-medium text-gray-700 dark:text-gray-400">Salary</p>
                   <span class="flex flex-col gap-0.5">
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 0.585167C4.21057 0.300808 3.78943 0.300807 3.59038 0.585166L1.05071 4.21327C0.81874 4.54466 1.05582 5 1.46033 5H6.53967C6.94418 5 7.18126 4.54466 6.94929 4.21327L4.40962 0.585167Z"/></svg>
                    <svg class="fill-gray-300 dark:fill-gray-700" width="8" height="5" viewBox="0 0 8 5" xmlns="http://www.w3.org/2000/svg"><path d="M4.40962 4.41483C4.21057 4.69919 3.78943 4.69919 3.59038 4.41483L1.05071 0.786732C0.81874 0.455343 1.05582 0 1.46033 0H6.53967C6.94418 0 7.18126 0.455342 6.94929 0.786731L4.40962 4.41483Z"/></svg>
                  </span>
                </div>
              </div>
            </div>

            <!-- Table Body -->
            <!-- Use <template> for v-for to avoid creating an extra DOM element -->
            <template v-if="paginatedData.length > 0">
              <div
                v-for="person in paginatedData"
                :key="person.id"
                class="grid grid-cols-12 border-t border-gray-100 dark:border-gray-800"
              >
                <!-- User Column -->
                <div class="col-span-3 flex items-center border-r border-gray-100 px-4 py-3 dark:border-gray-800">
                  <div class="flex items-center gap-3">
                    <div class="h-10 w-10 flex-shrink-0 overflow-hidden rounded-full">
                       <!-- Use :src for binding -->
                      <img :src="person.image" alt="user" />
                    </div>
                    <div>
                      <span class="block text-theme-sm font-medium text-gray-800 dark:text-white/90">{{ person.name }}</span>
                       <!-- You can add email or other details if available in your data -->
                       <!-- <span class="text-sm text-gray-500 dark:text-gray-400">{{ person.email }}</span> -->
                    </div>
                  </div>
                </div>
                <!-- Position Column -->
                <div class="col-span-2 flex items-center border-r border-gray-100 px-4 py-3 dark:border-gray-800">
                  <p class="text-theme-sm text-gray-700 dark:text-gray-400">{{ person.position }}</p>
                </div>
                <!-- Office Column -->
                <div class="col-span-2 flex items-center border-r border-gray-100 px-4 py-3 dark:border-gray-800">
                  <p class="text-theme-sm text-gray-700 dark:text-gray-400">{{ person.office }}</p>
                </div>
                <!-- Age Column -->
                <div class="col-span-1 flex items-center border-r border-gray-100 px-4 py-3 dark:border-gray-800">
                  <p class="text-theme-sm text-gray-700 dark:text-gray-400">{{ person.age }}</p>
                </div>
                <!-- Start Date Column -->
                <div class="col-span-2 flex items-center border-r border-gray-100 px-4 py-3 dark:border-gray-800">
                  <p class="text-theme-sm text-gray-700 dark:text-gray-400">{{ person.startDate }}</p>
                </div>
                <!-- Salary Column -->
                <div class="col-span-2 flex items-center px-4 py-3">
                  <p class="text-theme-sm text-gray-700 dark:text-gray-400">{{ person.salary }}</p>
                </div>
              </div>
            </template>
            <!-- Show message if no data matches search -->
            <div v-else class="border-t border-gray-100 dark:border-gray-800 px-4 py-4 text-center text-gray-500 dark:text-gray-400">
                No matching records found.
            </div>

          </div>
        </div>

        <!-- Pagination Controls -->
        <div class="border-t border-gray-100 py-4 pl-[18px] pr-4 dark:border-gray-800">
          <div class="flex flex-col xl:flex-row xl:items-center xl:justify-between">
            <p class="border-b border-gray-100 pb-3 text-center text-sm font-medium text-gray-500 dark:border-gray-800 dark:text-gray-400 xl:border-b-0 xl:pb-0 xl:text-left">
              Showing {{ startEntry }} to {{ endEntry }} of {{ totalEntries }} entries
            </p>

            <div class="flex items-center justify-center gap-0.5 pt-4 xl:justify-end xl:pt-0">
              <!-- Previous Button -->
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="mr-2.5 flex h-10 w-10 items-center justify-center rounded-lg border border-gray-300 bg-white text-gray-700 shadow-theme-xs hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03]"
              >
                <svg class="fill-current" width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M2.58301 9.99868C2.58272 10.1909 2.65588 10.3833 2.80249 10.53L7.79915 15.5301C8.09194 15.8231 8.56682 15.8233 8.85981 15.5305C9.15281 15.2377 9.15297 14.7629 8.86018 14.4699L5.14009 10.7472L16.6675 10.7472C17.0817 10.7472 17.4175 10.4114 17.4175 9.99715C17.4175 9.58294 17.0817 9.24715 16.6675 9.24715L5.14554 9.24715L8.86017 5.53016C9.15297 5.23717 9.15282 4.7623 8.85983 4.4695C8.56684 4.1767 8.09197 4.17685 7.79917 4.46984L2.84167 9.43049C2.68321 9.568 2.58301 9.77087 2.58301 9.99715C2.58301 9.99766 2.58301 9.99817 2.58301 9.99868Z" />
                </svg>
              </button>

              <!-- First Page Button -->
              <button
                @click="goToPage(1)"
                :class="currentPage === 1 ? 'bg-blue-500/[0.08] text-brand-500' : 'text-gray-700 dark:text-gray-400'"
                class="flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium hover:bg-blue-500/[0.08] hover:text-brand-500 dark:hover:text-brand-500"
              >
                1
              </button>

              <!-- Ellipsis Start -->
              <span v-if="currentPage > 3" class="flex h-10 w-10 items-center justify-center rounded-lg text-gray-700 dark:text-gray-400">...</span>

              <!-- Page Numbers -->
              <template v-for="page in pagesAroundCurrent" :key="page">
                <button
                  @click="goToPage(page)"
                  :class="currentPage === page ? 'bg-blue-500/[0.08] text-brand-500' : 'text-gray-700 dark:text-gray-400'"
                  class="flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium hover:bg-blue-500/[0.08] hover:text-brand-500 dark:hover:text-brand-500"
                >
                  {{ page }}
                </button>
              </template>

              <!-- Ellipsis End -->
               <span v-if="currentPage < totalPages - 2" class="flex h-10 w-10 items-center justify-center rounded-lg text-gray-700 dark:text-gray-400">...</span>

               <!-- Last Page Button (if needed and more than just a few pages) -->
               <button
                v-if="totalPages > 1"
                @click="goToPage(totalPages)"
                :class="currentPage === totalPages ? 'bg-blue-500/[0.08] text-brand-500' : 'text-gray-700 dark:text-gray-400'"
                class="flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium hover:bg-blue-500/[0.08] hover:text-brand-500 dark:hover:text-brand-500"
               >
                 {{ totalPages }}
               </button>


              <!-- Next Button -->
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="ml-2.5 flex h-10 w-10 items-center justify-center rounded-lg border border-gray-300 bg-white text-gray-700 shadow-theme-xs hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03]"
              >
                 <svg class="fill-current" width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M17.4175 9.9986C17.4178 10.1909 17.3446 10.3832 17.198 10.53L12.2013 15.5301C11.9085 15.8231 11.4337 15.8233 11.1407 15.5305C10.8477 15.2377 10.8475 14.7629 11.1403 14.4699L14.8604 10.7472L3.33301 10.7472C2.91879 10.7472 2.58301 10.4114 2.58301 9.99715C2.58301 9.58294 2.91879 9.24715 3.33301 9.24715L14.8549 9.24715L11.1403 5.53016C10.8475 5.23717 10.8477 4.7623 11.1407 4.4695C11.4336 4.1767 11.9085 4.17685 12.2013 4.46984L17.1588 9.43049C17.3173 9.568 17.4175 9.77087 17.4175 9.99715C17.4175 9.99763 17.4175 9.99812 17.4175 9.9986Z" />
                 </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- DataTable Component End -->
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// --- Reactive State ---
const search = ref('');
const sortColumn = ref('name'); // Default sort column
const sortDirection = ref('asc'); // Default sort direction ('asc' or 'desc')
const currentPage = ref(1);
const perPage = ref(10); // Default items per page

// --- Sample Data (Hardcoded as in the original example) ---
// In a real app, fetch this from an API (e.g., using onMounted hook)
const data = ref([
    { id: 1, name: "Lindsey Curtis", image: "src/images/user/user-17.jpg", position: "Sales Assistant", office: "New York", age: 33, startDate: "12 Feb, 2027", salary: "$168,500" },
    { id: 2, name: "Kaiya George", image: "src/images/user/user-18.jpg", position: "Sales Assistant", office: "San Francisco", age: 66, startDate: "13 Mar, 2027", salary: "$23,500" },
    { id: 3, name: "Zain Geidt", image: "src/images/user/user-19.jpg", position: "Sales Assistant", office: "Tokyo", age: 48, startDate: "19 Mar, 2027", salary: "$12,500" },
    { id: 4, name: "Abram Schleifer", image: "src/images/user/user-20.jpg", position: "Sales Assistant", office: "Edinburgh", age: 57, startDate: "25 Apr, 2027", salary: "$89,500" },
    { id: 5, name: "Carla George", image: "src/images/user/user-21.jpg", position: "Sales Assistant", office: "London", age: 45, startDate: "11 May, 2027", salary: "$15,500" },
    { id: 6, name: "Emery Culhane", image: "src/images/user/user-22.jpg", position: "Sales Assistant", office: "New York", age: 45, startDate: "29 Jun, 2027", salary: "$23,500" },
    { id: 7, name: "Livia Donin", image: "src/images/user/user-23.jpg", position: "Sales Assistant", office: "London", age: 26, startDate: "22 Jul, 2027", salary: "$58,500" }, // Corrected salary
    { id: 8, name: "Miracle Bator", image: "src/images/user/user-24.jpg", position: "Sales Assistant", office: "Tokyo", age: 38, startDate: "05 Aug, 2027", salary: "$34,900" },
    { id: 9, name: "Lincoln Herwitz", image: "src/images/user/user-25.jpg", position: "Sales Assistant", office: "London", age: 34, startDate: "09 Sep, 2027", salary: "$18,300" },
    { id: 10, name: "Ekstrom Bothman", image: "src/images/user/user-26.jpg", position: "Sales Assistant", office: "San Francisco", age: 53, startDate: "15 Nov, 2027", salary: "$19,200" },
    // Add more data items (up to 30 as in the original example)
    { id: 11, name: "Davis Calzoni", image: "src/images/user/user-17.jpg", position: "Developer", office: "New York", age: 29, startDate: "12 Feb, 2027", salary: "$118,500" },
    { id: 12, name: "Maria Rossi", image: "src/images/user/user-18.jpg", position: "Designer", office: "San Francisco", age: 31, startDate: "13 Mar, 2027", salary: "$93,500" },
    { id: 13, name: "Chen Wei", image: "src/images/user/user-19.jpg", position: "Accountant", office: "Tokyo", age: 42, startDate: "19 Mar, 2027", salary: "$102,500" },
    { id: 14, name: "Ahmed Khan", image: "src/images/user/user-20.jpg", position: "Engineer", office: "Edinburgh", age: 35, startDate: "25 Apr, 2027", salary: "$129,500" },
    { id: 15, name: "Sofia Garcia", image: "src/images/user/user-21.jpg", position: "Manager", office: "London", age: 40, startDate: "11 May, 2027", salary: "$145,500" },
    { id: 16, name: "Ken Tanaka", image: "src/images/user/user-22.jpg", position: "Analyst", office: "New York", age: 28, startDate: "29 Jun, 2027", salary: "$83,500" },
    { id: 17, name: "Fatima Dubois", image: "src/images/user/user-23.jpg", position: "Consultant", office: "London", age: 39, startDate: "22 Jul, 2027", salary: "$115,500" },
    { id: 18, name: "Liam O'Malley", image: "src/images/user/user-24.jpg", position: "Support", office: "Tokyo", age: 32, startDate: "05 Aug, 2027", salary: "$74,900" },
    { id: 19, name: "Isabelle Moreau", image: "src/images/user/user-25.jpg", position: "HR Specialist", office: "London", age: 36, startDate: "09 Sep, 2027", salary: "$98,300" },
    { id: 20, name: "Javier Fernandez", image: "src/images/user/user-26.jpg", position: "Marketing", office: "San Francisco", age: 44, startDate: "15 Nov, 2027", salary: "$109,200" },
     // ... Add items 21-30 if needed
]);

// --- Computed Properties ---

// Filtered and Sorted Data
const filteredData = computed(() => {
  const searchLower = search.value.toLowerCase();
  // Filter
  let filtered = data.value;
  if (searchLower) {
    filtered = data.value.filter(person =>
      person.name.toLowerCase().includes(searchLower) ||
      person.position.toLowerCase().includes(searchLower) ||
      person.office.toLowerCase().includes(searchLower)
    );
  }

  // Sort
  // Create a shallow copy before sorting to avoid mutating the original ref array directly
  return [...filtered].sort((a, b) => {
    let modifier = sortDirection.value === 'asc' ? 1 : -1;
    // Basic comparison, might need refinement for dates or currency
    if (a[sortColumn.value] < b[sortColumn.value]) return -1 * modifier;
    if (a[sortColumn.value] > b[sortColumn.value]) return 1 * modifier;
    return 0;
  });
});

// Data for the Current Page
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * perPage.value;
  const end = start + perPage.value;
  return filteredData.value.slice(start, end);
});

// Total Number of Pages
const totalPages = computed(() => {
  return Math.ceil(filteredData.value.length / perPage.value);
});

// Total Filtered Entries
const totalEntries = computed(() => filteredData.value.length);

// Start Entry Index for Display
const startEntry = computed(() => {
  if (totalEntries.value === 0) return 0;
  return (currentPage.value - 1) * perPage.value + 1;
});

// End Entry Index for Display
const endEntry = computed(() => {
  const end = currentPage.value * perPage.value;
  return end > totalEntries.value ? totalEntries.value : end;
});

// Calculate page numbers to display around the current page
const pagesAroundCurrent = computed(() => {
  let pages = [];
  // Determine start and end pages for the pagination block
  const maxVisibleButtons = 3; // Number of page buttons to show around current (excluding first/last)
  let startPage = Math.max(2, currentPage.value - Math.floor(maxVisibleButtons / 2));
  let endPage = Math.min(totalPages.value - 1, currentPage.value + Math.floor(maxVisibleButtons / 2));

   // Adjust if near the start
  if (currentPage.value <= 3) {
      endPage = Math.min(totalPages.value - 1, 1 + maxVisibleButtons);
  }
   // Adjust if near the end
  if (currentPage.value >= totalPages.value - 2) {
      startPage = Math.max(2, totalPages.value - maxVisibleButtons);
  }


  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }
  return pages;
});


// --- Methods ---

// Change Sort Column and Direction
function sortBy(column) {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortColumn.value = column;
    sortDirection.value = 'asc';
  }
  currentPage.value = 1; // Reset to first page on sort
}

// Go to Next Page
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}

// Go to Previous Page
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

// Go to Specific Page
function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

</script>

<style scoped>
/* Add any component-specific styles here if needed, though Tailwind handles most */
/* Ensure stroke is set for SVGs if Tailwind doesn't cover it */
svg path[stroke] {
    stroke: currentColor;
}
svg path[fill] {
    fill: currentColor;
}
</style>