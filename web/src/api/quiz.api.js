import api from './api.js'

// 获取题目组
export const getQuestionGroups = async () => {
  try {
    const response = await api.get('/quiz/question-groups/')
    return response.data
  } catch (error) {
    console.error('获取题目组失败:', error)
    throw error
  }
}

// 获取所有题目（不分组）
export const getAllQuestions = async () => {
  try {
    const response = await api.get('/quiz/all-questions/')
    return response.data
  } catch (error) {
    console.error('获取所有题目失败:', error)
    throw error
  }
}

// 创建测验会话
export const createQuizSession = async () => {
  try {
    const response = await api.post('/quiz/sessions/')
    return response.data
  } catch (error) {
    console.error('创建测验会话失败:', error)
    throw error
  }
}

// 保存用户答案
export const saveUserAnswer = async (sessionId, questionId, answer) => {
  try {
    const response = await api.post(`/quiz/sessions/${sessionId}/answers/`, {
      question_id: questionId,
      value: answer
    })
    return response.data
  } catch (error) {
    console.error('保存答案失败:', error)
    throw error
  }
}

// 完成测验会话
export const completeQuizSession = async (sessionId) => {
  try {
    const response = await api.post(`/quiz/sessions/${sessionId}/complete/`)
    return response.data
  } catch (error) {
    console.error('完成测验失败:', error)
    throw error
  }
}

// 获取用户历史测验记录
export const getQuizHistory = async () => {
  try {
    const response = await api.get('/quiz/sessions/history/')
    return response
  } catch (error) {
    console.error('获取历史记录失败:', error)
    throw error
  }
}

// 检查用户是否有未完成的测验会话
export const checkIncompleteSession = async () => {
  try {
    const response = await api.get('/quiz/sessions/check-incomplete/')
    return response
  } catch (error) {
    console.error('检查未完成会话失败:', error)
    throw error
  }
}

// 继续未完成的测验会话
export const resumeIncompleteSession = async (sessionId) => {
  try {
    // console.log('🔄 调用resumeIncompleteSession API，sessionId:', sessionId)
    // 获取会话详情（包含答案信息）
    const response = await api.get(`/quiz/sessions/${sessionId}/`)
    // console.log('✅ 从后端获取的原始数据:', response.data)
    
    // 构建前端需要的答案格式
    const answerMap = {};
    if (response.data.answers && Array.isArray(response.data.answers)) {
      // console.log('📊 处理答案数据，数组长度:', response.data.answers.length)
      response.data.answers.forEach(answer => {
        // 将答案对象转换为前端需要的格式
        // 检查value是否为JSON字符串，如果是则解析
        let answerValue = answer.value;
        try {
          if (typeof answerValue === 'string' && 
              (answerValue.startsWith('{') || answerValue.startsWith('['))) {
            answerValue = JSON.parse(answerValue);
          }
        } catch (e) {
          // 如果解析失败，保持原值
          console.warn('解析答案值失败:', e);
        }
        answerMap[answer.question_id] = answerValue;
        // console.log('🔑 映射问题ID:', answer.question_id, '到答案:', answerValue)
      });
    }
    
    // console.log('✅ 构建的答案映射对象:', answerMap)
    return {
      session: response.data,
      answers: answerMap
    }
  } catch (error) {
    // console.error('继续会话失败:', error)
    throw error
  }
}

// 获取测验报告
export const getQuizReport = async (sessionId) => {
  try {
    const response = await api.get(`/quiz/sessions/${sessionId}/report/`)
    return response
  } catch (error) {
    console.error('获取测验报告失败:', error)
    throw error
  }
}

// 删除未完成的测验会话
export const deleteIncompleteSession = async (sessionId) => {
  try {
    const response = await api.delete(`/quiz/sessions/${sessionId}/`)
    return response.data
  } catch (error) {
    console.error('删除测验会话失败:', error)
    throw error
  }
}

// 使用AI扩写文本
export const extendTextWithAI = async (text) => {
  try {
    const response = await api.post('/quiz/extend-text-with-ai/', {
      text: text
    })
    return response.data
  } catch (error) {
    console.error('AI扩写失败:', error)
    throw error
  }
}