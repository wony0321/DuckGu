import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useMovieStore = defineStore('movie', () => {
  
  const router = useRouter()
  const token = ref(null)
  const groups = ref([])
  const keywords = ref([])
  const joinedGroups = ref([])
  const groupDetail = ref([])
  const user = ref(null)
  const userId = ref(null)
  const filteredMovies = ref([])

  const API_URL = 'http://127.0.0.1:8000'

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })


  const signUp = function (payload) {

    const { username, email, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, email, password1, password2
      }
    })
      .then((response) => {
        token.value = response.data.key
        const password = password1
        logIn({username, password})
        console.log('회원가입 성공!')
      })
      .catch((error) => {
        alert('🐣정보를 잘못 입력했습니덕🐣')
        console.log(error)
      })
  }


  const logIn = async function (payload) {
    const { username, password } = payload
  
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: {
          username, password
        }
      })
      token.value = response.data.key
      console.log('로그인 성공')
      
      // 로그인 성공 후 사용자 정보 가져오기
      getUserInfo(username)
      
      router.push({ name: 'home' })
    } catch (error) {
      alert('🐣아이디 또는 비밀번호를 잘못 입력했습니덕🐣')
      console.log(error)
    }
  }
  
  
  const getUserInfo = function (username) {
    axios({
      method: 'get',
      url: `${API_URL}/user/profile/${username}/`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
      params: {
        username
      }
    })
    .then((res) => {
      user.value = res.data
      console.log('사용자 정보:', res.data)
    })
    .catch((err) => {
      console.log(err)
    })
  }

  const logOut = function() {
    token.value = null
    user.value = null
    console.log('로그아웃 성공')
    router.push({ name: 'home' })
  }

  const getGroups = function () {
    axios({
      method: 'get',
      url: `${API_URL}/duck9/meet/`,
    })
      .then((response) => {
        groups.value = response.data.meets
        keywords.value = response.data.keywords_list
        // console.log('Meets:', groups)
        // console.log('Keywords List:', keywords)
        // console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }


  const createMeet = function (payload) {
    if (!isLogin.value) {
      alert('로그인이 필요합니다.');
      return;
    }
  
    axios({
      method: 'post',
      url: `${API_URL}/duck9/meet/`,
      data: payload,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
    .then((response) => {
      console.log('Meet created successfully:', response.data);
      // groups.value.push(response.data)
      alert('모임이 생성되었습니다.')
      router.push({ name: 'joined' })
    })
    .catch((error) => {
      console.log(error.response.data)
      alert('모임 생성에 실패했습니다.')
    })
  }
  

  const getJoinedGroups = function () {
    axios({
      method: 'get',
      url: `${API_URL}/duck9/joined_meets/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((response) => {
        // console.log(response.data)
        joinedGroups.value = response.data.reverse()
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const modifyMeet = function (meet_id, action) {
    axios({
      method: action,
      url: `${API_URL}/duck9/join_meet/${meet_id}/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
    .then((response) => {
      // console.log(response.data)
      const message = action === 'post' ? '참가되었습니덕' : '탈퇴되었습니덕';
      alert(`${response.data.name}에서 ${message}`)
      getJoinedGroups()  // 업데이트된 joined groups 목록 가져오기
      router.push({name: 'joined'})
    })
    .catch((error) => {
      console.log(error);
    });
  }

  const getGroupDetail = async function (meet_id) {
    console.log("getGroupDetail called with meet_id:", meet_id)// 디버깅용 로그
    console.log("Using token:", token.value)
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/duck9/meet/${meet_id}/`,
        headers: {
          'Authorization': `Token ${token.value}`
        }
      });
      groupDetail.value = response.data;
      console.log("Group detail response:", response.data); // 디버깅용 로그
    } catch (error) {
      console.error("Error fetching group detail:", error); // 에러 로그
    }
  }

  const getReviews = function (movie_pk) {
    axios({
      method: 'get',
      url: `${API_URL}/duck9/meet/${movie_pk}/review/`,
    })
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const getMoviesByKeywords = function (keywordIds) {
    // console.log("Sending keywordIds:", keywordIds)
    axios({
      method: 'get',
      url: `${API_URL}/duck9/movie/`,
      params: {
        keywords: keywordIds.join(',')
      }
    })
      .then((response) => {
        filteredMovies.value = response.data
        console.log('Filtered Movies:', filteredMovies.value)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const meetUpdateAndDelete = function (meet_id, payload, action) {
    axios({
      method: action,
      url: `${API_URL}/duck9/meet/${meet_id}/`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
      data: payload
    }).then(response => {
      console.log('수정 성공:', response.data)
      const meetMessage = action === 'put' ? '수정되었습니덕' : '삭제되었습니덕';
      alert(`모임이 ${meetMessage}`)
      getGroups()  // 업데이트된 joined groups 목록 가져오기
      router.push({name: 'joined'})
    })
    .catch(error => {
      console.error('실패했습니덕:', error)
    })
  }


  return { 
    API_URL, 
    router,
    token,
    groups,
    keywords,
    joinedGroups,
    groupDetail,
    isLogin,
    user,
    userId,
    filteredMovies,
    signUp, 
    logIn, 
    logOut, 
    getGroups,
    createMeet,
    getJoinedGroups,
    modifyMeet,
    getGroupDetail,
    getReviews,
    getMoviesByKeywords,
    getUserInfo,
    meetUpdateAndDelete,
   }
}, {
  persist: {
    key: 'movie-store',
    storage: localStorage,
  }
})
