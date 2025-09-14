// @/composables/product.js
import { ref } from 'vue'

export const product = () => {
  const perfumes = ref([
    {
      id: 1,
      name: '晨曦之露',
      image: 'https://picsum.photos/id/96/600/400',
      description: '清新的柑橘与晨露草香，带来清晨的宁静与希望，驱散不安情绪。',
      mood: '舒缓焦虑',
      notes: ['柑橘调', '草本', '清新'],
      price: '¥568'
    },
    {
      id: 2,
      name: '森林低语',
      image: 'https://picsum.photos/id/118/600/400',
      description: '深邃的木质香调与苔藓气息，如同置身宁静森林，带来安全感与稳定感。',
      mood: '缓解抑郁',
      notes: ['木质调', '苔藓', '沉稳'],
      price: '¥628'
    },
    {
      id: 3,
      name: '海洋呼吸',
      image: 'https://picsum.photos/id/152/600/400',
      description: '清新的海洋气息与海盐香，带来开阔感与活力，驱散疲惫与低落。',
      mood: '提升活力',
      notes: ['海洋调', '海盐', '清爽'],
      price: '¥588'
    },
    {
      id: 4,
      name: '薰衣草梦境',
      image: 'https://picsum.photos/id/175/600/400',
      description: '纯净的薰衣草与洋甘菊，舒缓神经，平复思绪，帮助安然入睡。',
      mood: '改善睡眠',
      notes: ['花香调', '薰衣草', '舒缓'],
      price: '¥548'
    },
    {
      id: 5,
      name: '阳光柑橘',
      image: 'https://picsum.photos/id/237/600/400',
      description: '活力四射的柑橘与佛手柑，带来阳光般的温暖与愉悦，驱散阴霾。',
      mood: '提升心情',
      notes: ['柑橘调', '佛手柑', '活力'],
      price: '¥528'
    },
    {
      id: 6,
      name: '禅意檀香',
      image: 'https://picsum.photos/id/240/600/400',
      description: '醇厚的檀香与琥珀，营造冥想般的宁静氛围，帮助专注与内省。',
      mood: '冥想平静',
      notes: ['木质调', '檀香', '宁静'],
      price: '¥668'
    }
  ])

  return { perfumes }
}