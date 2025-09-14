// 香水数据
const perfumeData = {
  "晨曦之露": {
    image: "https://picsum.photos/id/96/600/400",
    description: "清新的柑橘与晨露草香，带来清晨的宁静与希望，驱散不安情绪。",
    price: 568,
    usage: {
      daily: "适合每天早晨使用，喷洒在衣领和手腕处，让清新的香气伴随你开启充满希望的一天。",
      work: "工作前喷洒在办公室周围或手帕上，帮助保持清醒和平静，提高工作效率。",
      relax: "冥想或放松时使用，配合深呼吸，让清新的香气帮助你进入平静状态。",
      sleep: "虽然不是专门的助眠香氛，但它的清新气息也能帮助一些人放松入睡。"
    }
  },
  "森林低语": {
    image: "https://picsum.photos/id/118/600/400",
    description: "深邃的木质香调与苔藓气息，如同置身宁静森林，带来安全感与稳定感。",
    price: 628,
    usage: {
      daily: "适合在感到需要稳定感的日子使用，少量喷洒即可带来持久的舒适感。",
      work: "在高压工作环境中使用，帮助营造稳定、专注的氛围，减轻工作压力。",
      relax: "非常适合放松时使用，尤其适合在阅读或品茶时，增强宁静感。",
      sleep: "睡前少量使用，其沉稳的木质调能带来安全感，帮助放松入睡。"
    }
  },
  "海洋呼吸": {
    image: "https://picsum.photos/id/152/600/400",
    description: "清新的海洋气息与海盐香，带来开阔感与活力，驱散疲惫与低落。",
    price: 588,
    usage: {
      daily: "适合在闷热或情绪低落的日子使用，带来清新开阔的感觉。",
      work: "午后感到疲惫时使用，帮助提神醒脑，恢复工作活力。",
      relax: "洗澡后使用，配合轻柔的音乐，仿佛置身海边，带来放松与开阔感。",
      sleep: "对于喜欢清新气息的人，少量使用可以创造舒适的睡眠环境。"
    }
  },
  "薰衣草梦境": {
    image: "https://picsum.photos/id/175/600/400",
    description: "纯净的薰衣草与洋甘菊，舒缓神经，平复思绪，帮助安然入睡。",
    price: 548,
    usage: {
      daily: "适合在感到焦虑的日子全天使用，帮助保持平静。",
      work: "在紧张的会议前使用，帮助平复紧张情绪，保持冷静。",
      relax: "泡澡或冥想时使用，增强放松效果，舒缓紧张神经。",
      sleep: "睡前喷洒在枕头和床单上，帮助放松身心，改善睡眠质量，是失眠者的理想选择。"
    }
  },
  "阳光柑橘": {
    image: "https://picsum.photos/id/237/600/400",
    description: "活力四射的柑橘与佛手柑，带来阳光般的温暖与愉悦，驱散阴霾。",
    price: 528,
    usage: {
      daily: "特别适合阴雨天或情绪低落时使用，带来阳光般的活力。",
      work: "早晨使用，帮助提升精神状态和积极情绪，迎接一天的工作挑战。",
      relax: "进行户外活动或社交活动前使用，提升愉悦感和社交自信。",
      sleep: "不建议睡前大量使用，少量使用对部分人也能带来愉悦的入睡体验。"
    }
  },
  "禅意檀香": {
    image: "https://picsum.photos/id/240/600/400",
    description: "醇厚的檀香与琥珀，营造冥想般的宁静氛围，帮助专注与内省。",
    price: 668,
    usage: {
      daily: "适合需要保持内心平静的日子，带来持久的宁静感。",
      work: "需要高度专注的工作前使用，帮助集中注意力，提高工作效率。",
      relax: "非常适合冥想、瑜伽或阅读时使用，增强内心的平静与专注。",
      sleep: "睡前使用，其醇厚的香气能带来深沉的放松感，帮助进入深度睡眠。"
    }
  }
};

// 用户评价数据
const testimonials = [
  {
    id: 1,
    imageSrc: "https://picsum.photos/id/64/100/100",
    name: "林小姐",
    location: "上海",
    text: "薰衣草梦境真的改变了我的睡眠质量，之前总是失眠焦虑，现在能更快入睡了。",
    product: "薰衣草梦境",
    rating: 5
  },
  {
    id: 2,
    imageSrc: "https://picsum.photos/id/65/100/100",
    name: "王先生",
    location: "北京",
    text: "工作压力大的时候，禅意檀香的味道能让我瞬间平静下来，提高工作效率。",
    product: "禅意檀香",
    rating: 4
  },
  {
    id: 3,
    imageSrc: "https://picsum.photos/id/66/100/100",
    name: "张女士",
    location: "广州",
    text: "情绪低落的时候，阳光柑橘的味道真的像阳光一样照亮了我的心情，非常推荐！",
    product: "阳光柑橘",
    rating: 5
  }
];

export function usePerfumes() {
  // 获取所有香水列表
  function getPerfumeList() {
    return Object.keys(perfumeData).map(key => ({
      name: key,
      ...perfumeData[key]
    }));
  }
  
  // 获取单款香水详情
  function getPerfumeDetail(name) {
    return perfumeData[name] ? { name, ...perfumeData[name] } : null;
  }
  
  // 获取完整的香水数据
  function getPerfumeData() {
    return { ...perfumeData };
  }
  
  // 获取用户评价
  function getTestimonials() {
    return [...testimonials];
  }
  
  return {
    getPerfumeList,
    getPerfumeDetail,
    getPerfumeData,
    getTestimonials
  };
}
