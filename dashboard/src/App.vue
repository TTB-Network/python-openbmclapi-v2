<script setup lang="ts">
import Menubar from 'primevue/menubar'
import { RouterView } from 'vue-router'
import { ref } from 'vue'
import Button from 'primevue/button'
const items = ref([
    {
        label: '主页',
        icon: 'pi pi-home',
        url: '/dashboard'
    },
    {
        label: '排行',
        icon: 'pi pi-trophy',
        url: '/dashboard/rank'
    },
    {
        label: 'GitHub',
        icon: 'pi pi-github',
        url: 'https://github.com/SilianZ/one-openbmclapi-dashboard'
    }
])

</script>

<template>
    <div id="menu">
        <Menubar :model="items" id="menubar">
            <template #start>
                <img src="/logo.svg" style="height: 30px" />
            </template>
        </Menubar>
    </div>
    <div id="body">
        <RouterView />
    </div>
</template>

<style scoped>
#body {
    padding: 1rem 2rem 4rem 2rem;
    min-height: 100vh;
}

#menu {
    margin: 18px
}

.button {
    border-radius: 0.5rem;
}

#menubar {
    border-radius: 0.5rem;
}

@media screen and (max-width: 720px) {
    #body {
        padding: 20px;
        min-height: 100vh;
    }
}
</style>
