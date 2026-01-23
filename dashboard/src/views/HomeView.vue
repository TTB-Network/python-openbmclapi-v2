<script setup lang="ts">
import StatsComponent from '../component/StatsComponent.vue'
import ChartsComponent from '../component/ChartsComponent.vue'
import { type StatsRes } from '../api'
import { useRequest } from 'vue-request'
import { fetchStat } from '../api'
import { ref } from 'vue'
import { watch } from 'vue'

const { data, refresh, loading, error } = useRequest((): Promise<StatsRes> => fetchStat(), { 
    pollingInterval: 5000, // Poll every 5 seconds for real-time updates
    refreshOnWindowFocus: true // Refresh when user returns to tab
})

const stats = ref<StatsRes | null>(null)

watch(
    () => data.value,
    (newData) => {
        if (!newData) {
            stats.value = null
            return
        }
        stats.value = newData
    }
)
</script>

<template>
    <div class="flex justify-between items-center mb-4">
        <h1>主页</h1>
        <button 
            @click="refresh" 
            :disabled="loading"
            class="refresh-btn px-4 py-2 rounded-lg transition-colors"
            :class="loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100 dark:hover:bg-gray-800'"
        >
            <i class="pi pi-refresh" :class="loading ? 'pi-spin' : ''"></i>
            刷新
        </button>
    </div>
    <div v-if="error" class="error-message p-4 mb-4 rounded-lg bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
        <i class="pi pi-exclamation-triangle mr-2"></i>
        加载数据时出错，请稍后重试
    </div>
    <StatsComponent :data="stats" />
    <ChartsComponent :data="stats" />
</template>

<style scoped>
h1 {
    display: block;
    font-size: 2em;
    margin-block-start: 0.67em;
    margin-block-end: 0.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.refresh-btn {
    border: 1px solid var(--p-content-border-color);
    background: var(--p-content-background);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.error-message {
    display: flex;
    align-items: center;
}

@media screen and (max-width: 720px) {
    h1 {
        font-size: 30px;
    }
    .refresh-btn {
        font-size: 14px;
        padding: 0.5rem 1rem;
    }
}
</style>
