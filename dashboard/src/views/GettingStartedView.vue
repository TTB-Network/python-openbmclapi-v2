<script setup lang="ts">
import Card from "primevue/card";
import Button from "primevue/button";
import { ref, computed } from "vue";
import { z } from "zod";
import { postConfig, Config } from "../api";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import { Form, FormSubmitEvent } from "@primevue/forms";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import Message from "primevue/message";

const initialValues = ref<Config>({
    language: "",
    clusterId: "",
    clusterSecret: "",
    byoc: false,
    host: undefined,
    username: "",
    password: "",
});

const languageOptions = [
    {
        code: "zh_cn",
        label: "简体中文",
    },
    {
        code: "en_us",
        label: "English (US)",
    },
];

const byocOptions = [
    {
        code: true,
        label: "启用 BYOC",
    },
    {
        code: false,
        label: "禁用 BYOC",
    },
];

const resolver = computed(() => {
    switch (key.value) {
        case 1:
            return zodResolver(
                z.object({
                    language: z.string().min(1, { message: "请设置语言。" }),
                }),
            );
        case 2:
            return zodResolver(
                z.object({
                    username: z
                        .string()
                        .min(1, { message: "请设置用户名。" })
                        .regex(/^[A-Za-z_]+$/, {
                            message: "只能包含大小写字母和下划线。",
                        }),
                    password: z.string().min(1, { message: "请设置密码。" }),
                }),
            );
        case 3:
            return zodResolver(
                z.object({
                    clusterId: z
                        .string()
                        .min(1, { message: "请设置节点 ID。" })
                        .regex(/^[a-z0-9]+$/, {
                            message: "只能包含数字或小写字母。",
                        }),
                    clusterSecret: z
                        .string()
                        .min(1, { message: "请设置节点 Secret。" })
                        .regex(/^[a-z0-9]+$/, {
                            message: "只能包含数字或小写字母。",
                        }),
                    host: z
                        .string({ message: "请设置域名。" })
                        .regex(/^(?!:\/\/)([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}$/, {
                            message: "这不是一个合法的域名。",
                        })
                        .optional()
                }),
            );
    }
});

const onNextPage = (e: FormSubmitEvent) => {
    if (!e.valid) {
        return;
    }
    initialValues.value = { ...initialValues.value, ...(e.values as Config) };
    console.log(initialValues.value)
    key.value++;
};
const key = ref(0);
</script>

<template>
    <div class="flex flex-col justify-center items-center">
        <h1>快速开始</h1>
        <Card class="w-[25rem]">
            <template #content>
                <div class="m-4">
                    <div
                        v-if="key == 0"
                        class="flex flex-col justify-center items-center gap-4"
                    >
                        <img src="/logo.svg" width="200px" />
                        <p class="text-center">欢迎使用 Python OpenBMCLAPI！</p>
                        <p class="text-center">让我们开始吧！</p>
                        <Button class="w-full" @click="key++">开始</Button>
                    </div>
                    <div
                        v-if="key == 1"
                        class="flex flex-col justify-center items-center"
                    >
                        <Form
                            v-slot="$form"
                            :resolver
                            :initialValues
                            @submit="onNextPage"
                            class="flex flex-col w-full justify-center items-center gap-8 m-4"
                        >
                            <h2 class="text-center">设置语言</h2>
                            <div class="flex flex-col gap-2 w-full">
                                <Select
                                    name="language"
                                    :options="languageOptions"
                                    class="w-full"
                                    optionLabel="label"
                                    optionValue="code"
                                    placeholder="语言 / Language"
                                />
                                <Message
                                    v-if="$form.language?.invalid"
                                    severity="error"
                                    size="small"
                                    variant="simple"
                                    >{{ $form.language.error.message }}</Message
                                >
                            </div>
                            <div class="flex gap-4 w-full">
                                <Button
                                    severity="secondary"
                                    class="w-full"
                                    @click="key--"
                                    >上一页</Button
                                >
                                <Button class="w-full" type="submit"
                                    >下一页</Button
                                >
                            </div>
                        </Form>
                    </div>
                    <div
                        v-if="key == 2"
                        class="flex flex-col justify-center items-center"
                    >
                        <Form
                            v-slot="$form"
                            :resolver
                            :initialValues
                            @submit="onNextPage"
                            class="flex flex-col w-full justify-center items-center gap-8 m-4"
                        >
                            <h2 class="text-center">设置面板的用户名和密码</h2>
                            <div class="flex flex-col gap-2 w-full">
                                <InputText
                                    name="username"
                                    type="text"
                                    placeholder="用户名"
                                    autocomplete="username"
                                    class="w-full"
                                />
                                <Message
                                    v-if="$form.username?.invalid"
                                    severity="error"
                                    size="small"
                                    variant="simple"
                                    >{{ $form.username.error.message }}</Message
                                >
                            </div>
                            <div class="flex flex-col gap-2 w-full">
                                <InputText
                                    name="password"
                                    type="password"
                                    placeholder="密码"
                                    autocomplete="new-password"
                                    class="w-full"
                                />
                                <Message
                                    v-if="$form.password?.invalid"
                                    severity="error"
                                    size="small"
                                    variant="simple"
                                    >{{ $form.password.error.message }}</Message
                                >
                            </div>
                            <div class="flex gap-4 w-full">
                                <Button
                                    severity="secondary"
                                    class="w-full"
                                    @click="key--"
                                    >上一页</Button
                                >
                                <Button class="w-full" type="submit"
                                    >下一页</Button
                                >
                            </div>
                        </Form>
                    </div>
                    <div
                        v-if="key == 3"
                        class="flex flex-col justify-center items-center"
                    >
                        <Form
                            v-slot="$form"
                            :resolver
                            :initialValues
                            @submit="onNextPage"
                            class="flex flex-col w-full justify-center items-center gap-8 m-4"
                        >
                            <h2 class="text-center">设置节点信息</h2>
                            <div class="flex flex-col gap-2 w-full">
                                <InputText
                                    name="clusterId"
                                    type="text"
                                    placeholder="节点 ID"
                                    class="w-full"
                                />
                                <Message
                                    v-if="$form.clusterId?.invalid"
                                    severity="error"
                                    size="small"
                                    variant="simple"
                                    >{{
                                        $form.clusterId.error.message
                                    }}</Message
                                >
                            </div>
                            <div class="flex flex-col gap-2 w-full">
                                <InputText
                                    name="clusterSecret"
                                    type="text"
                                    placeholder="节点 Secret"
                                    class="w-full"
                                />
                                <Message
                                    v-if="$form.clusterSecret?.invalid"
                                    severity="error"
                                    size="small"
                                    variant="simple"
                                    >{{
                                        $form.clusterSecret.error.message
                                    }}</Message
                                >
                            </div>
                            <Select
                                name="byoc"
                                placeholder="BYOC"
                                :options="byocOptions"
                                optionLabel="label"
                                optionValue="code"
                                class="w-full"
                            />
                            <div
                                v-if="$form.byoc?.value"
                                class="flex flex-col gap-2 w-full"
                            >
                                <InputText
                                    name="host"
                                    type="text"
                                    placeholder="域名"
                                    class="w-full"
                                />
                                <Message
                                    v-if="$form.host?.invalid"
                                    severity="error"
                                    size="small"
                                    variant="simple"
                                    >{{ $form.host.error.message }}</Message
                                >
                            </div>
                            <div class="flex gap-4 w-full">
                                <Button
                                    severity="secondary"
                                    class="w-full"
                                    @click="key--"
                                    >上一页</Button
                                >
                                <Button class="w-full" type="submit"
                                    >下一页</Button
                                >
                            </div>
                        </Form>
                    </div>
                    <div
                        v-if="key == 4"
                        class="flex flex-col justify-center items-center gap-4"
                    >
                            <h2 class="text-center">确认信息</h2>
                            <div class="flex flex-col gap-4 w-full">
                                <span><b class="font-bold">语言：</b>{{ initialValues.language == "zh_cn" ? "简体中文" : "English (US)" }}</span>
                                <span><b class="font-bold">用户名：</b>{{ initialValues.username }}</span>
                                <span><b class="font-bold">密码：</b>{{ initialValues.password }}</span>
                                <span><b class="font-bold">节点 ID：</b>{{ initialValues.clusterId }}</span>
                                <span><b class="font-bold">节点 Secret：</b>{{ initialValues.clusterSecret }}</span>
                            </div>
                            <div class="flex gap-4 w-full">
                                <Button
                                    severity="secondary"
                                    class="w-full"
                                    @click="key--"
                                    >上一页</Button
                                >
                                <Button class="w-full" type="submit"
                                    >下一页</Button
                                >
                            </div>
                    </div>
                </div>
            </template>
        </Card>
    </div>
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
h2 {
    display: block;
    font-size: 1.2em;
    margin-block-start: 0.67em;
    margin-block-end: 0.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}
</style>
