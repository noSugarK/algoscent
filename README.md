# demo

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


```text
src/
├── components/
│   ├── questionnaire/
│   │   ├── StepPathSelection.vue       ← 路径选择
│   │   ├── StepCustomBase.vue          ← 自定义流程（修改配方）
│   │   ├── StepUsedPerfume.vue         ← 是否用过香水
│   │   ├── StepFixedFormula.vue        ← 是否在固定配方上修改
│   │   ├── StepFavoritePerfumes.vue    ← 常用香水选择
│   │   ├── StepAcceptChange.vue        ← 是否接受风格改变
│   │   ├── StepPersonality.vue         ← 人格与敏感度
│   │   ├── StepRelaxScene.vue          ← 放松场景
│   │   ├── StepInputMethod.vue         ← 文字 or 图片输入
│   │   ├── StepToneDetails.vue         ← 香调细节
│   │   ├── StepMainTone.vue            ← 主调选择
│   │   ├── StepIngredient.vue          ← 成分选择
│   │   ├── StepRatio.vue               ← 配比确定
│   │   └── StepResult.vue              ← 结果生成
│   └── layout/
│       ├── AppHeader.vue
│       └── AppFooter.vue
├── composables/
│   └── usePerfumeFlow.js               ← 流程逻辑封装
└── views/
    └── PerfumeQuizView.vue             ← 主页面
```