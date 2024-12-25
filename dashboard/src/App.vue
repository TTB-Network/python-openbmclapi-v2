<script setup lang="ts">
import { RouterView } from "vue-router";
import Toast from "primevue/toast"
</script>

<template>
    <Toast />
    <div id="body">
        <div id="router-view">
            <RouterView />
        </div>
    </div>
</template>

<style scoped>
#router-view {
    padding: 1rem 2rem 4rem 2rem;
}
#body {
    margin: 14px;
}
</style>
