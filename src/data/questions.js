// src/data/questions.js
export const questionGroups = [
  // ============ Part 1: 多个单选题 ============
  {
    id: 'part1',
    title: '🌿 基础情绪与偏好',
    description: '请回答以下基础问题',
    questions: [
      {
        id: 'q1',
        text: '你最近的情绪基调是？',
        type: 'single',
        options: [
          { label: '焦虑不安，需要安抚', value: 'anxious', emoji: '😰' },
          { label: '平静放松，享受当下', value: 'calm', emoji: '😌' },
          { label: '充满活力，渴望探索', value: 'energetic', emoji: '🌟' }
        ]
      },
      {
        id: 'q2',
        text: '你更偏爱哪个季节？',
        type: 'single',
        options: [
          { label: '春天', value: 'spring', emoji: '🌸' },
          { label: '夏天', value: 'summer', emoji: '☀️' },
          { label: '秋天', value: 'autumn', emoji: '🍂' },
          { label: '冬天', value: 'winter', emoji: '❄️' }
        ]
      }
    ]
  },

  // ============ Part 2: 单选 + 条件填空 ============
  {
    id: 'part2',
    title: '🧴 香水使用习惯',
    description: '了解你的香水使用经验',
    questions: [
      {
        id: 'q3',
        text: '你是否使用过香水？',
        type: 'single-with-text',
        showTextWhen: 'yes', // 👈 新增：仅当选择 'yes' 时显示填空
        options: [
          { label: '有使用过', value: 'yes' },
          { label: '从未使用', value: 'no' }
        ],
        placeholder: '请填写你最常用的香水品牌或名称...'
      }
    ]
  },

  // ============ Part 3: 多个图片单选题 ============
  {
    id: 'part3',
    title: '🖼️ 视觉风格偏好（单选）',
    description: '每题选择一张最打动你的图片',
    questions: [
      {
        id: 'q5',
        text: '哪张图让你感到最放松？',
        type: 'image-single',
        options: [
          { label: '森林', value: 'forest', image: 'https://picsum.photos/id/10/400/300' },
          { label: '海洋', value: 'ocean', image: 'https://picsum.photos/id/20/400/300' },
          { label: '沙漠', value: 'desert', image: 'https://picsum.photos/id/30/400/300' }
        ]
      },
      {
        id: 'q6',
        text: '你更喜欢哪种室内风格？',
        type: 'image-single',
        options: [
          { label: '北欧极简', value: 'nordic', image: 'https://picsum.photos/id/40/400/300' },
          { label: '复古奢华', value: 'vintage', image: 'https://picsum.photos/id/50/400/300' },
          { label: '日式禅意', value: 'zen', image: 'https://picsum.photos/id/60/400/300' }
        ]
      }
    ]
  },

  // ============ Part 4: 多个图片多选题 ============
  {
    id: 'part4',
    title: '🎨 色彩与元素偏好（多选）',
    description: '每题可选1-3项',
    questions: [
      {
        id: 'q7',
        text: '哪些自然元素吸引你？',
        type: 'image-multiple',
        maxSelection: 3,
        options: [
          { label: '花', value: 'flower', image: 'https://picsum.photos/id/70/200/200' },
          { label: '木', value: 'wood', image: 'https://picsum.photos/id/80/200/200' },
          { label: '石', value: 'stone', image: 'https://picsum.photos/id/90/200/200' },
          { label: '水', value: 'water', image: 'https://picsum.photos/id/100/200/200' }
        ]
      },
      {
        id: 'q8',
        text: '你偏爱哪些色彩氛围？',
        type: 'image-multiple',
        maxSelection: 3,
        options: [
          { label: '薄荷绿', value: 'mint', image: 'https://picsum.photos/id/110/200/200' },
          { label: '琥珀橙', value: 'amber', image: 'https://picsum.photos/id/120/200/200' },
          { label: '星空蓝', value: 'blue', image: 'https://picsum.photos/id/130/200/200' },
          { label: '薰衣草紫', value: 'purple', image: 'https://picsum.photos/id/140/200/200' }
        ]
      }
    ]
  }
]