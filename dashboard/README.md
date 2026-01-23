# Python-OpenBMCLAPI Dashboard

基于 Vue 3 + TypeScript + Vite 构建的 Python-OpenBMCLAPI 仪表盘。

## 特性

- 🎨 使用 PrimeVue 组件库实现现代化 UI
- 📊 实时数据展示（每 5 秒自动刷新）
- 📱 响应式设计，支持移动设备
- 🌙 深色模式支持
- 📈 多维度统计图表
  - 当日/当月/当年请求统计
  - 用户分布分析
- ⚡ 性能监控
  - CPU 使用率
  - 内存使用情况
  - 连接数
  - 运行时间

## 技术栈

- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [TypeScript](https://www.typescriptlang.org/) - JavaScript 的超集
- [Vite](https://vitejs.dev/) - 新一代前端构建工具
- [PrimeVue](https://primevue.org/) - Vue UI 组件库
- [TailwindCSS](https://tailwindcss.com/) - 实用优先的 CSS 框架
- [Chart.js](https://www.chartjs.org/) - 图表库
- [Vue Router](https://router.vuejs.org/) - Vue.js 官方路由

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 格式化代码
npm run format
```

## 项目结构

```
dashboard/
├── src/
│   ├── api/          # API 接口定义
│   ├── component/    # 可复用组件
│   ├── router/       # 路由配置
│   ├── utils/        # 工具函数
│   └── views/        # 页面视图
├── public/           # 静态资源
└── index.html        # 入口 HTML
```

## IDE 支持

推荐使用 [VSCode](https://code.visualstudio.com/) 配合以下插件：
- [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (之前称为 Volar)
- [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)

## 类型支持

使用 Vue 3 `<script setup>` SFC，了解更多请参考 [script setup 文档](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup)。

更多关于项目设置和 IDE 支持的信息，请参考 [Vue 文档 TypeScript 指南](https://vuejs.org/guide/typescript/overview.html#project-setup)。
