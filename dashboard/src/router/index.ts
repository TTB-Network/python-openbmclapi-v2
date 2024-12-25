import { createRouter, createWebHistory } from "vue-router";
import GettingStartedView from "../views/GettingStartedView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/dashboard/getting-started",
            component: GettingStartedView,
        },
    ],
});

export default router;
