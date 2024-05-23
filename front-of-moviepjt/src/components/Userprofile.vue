<template>
  <div v-if="user">
    <h1>{{ user.username }} 님의 페이지입니다</h1>
    <div>
      <p>이름: {{ user.last_name }} {{ user.first_name }}</p>
      <div>
				<span>팔로잉: {{ followingCount }}명 |</span>
				<span>팔로워: {{ followerCount }}명 |</span>
				<button v-if="!isCurrentUser" @click="toggleFollow">
					{{ isFollowing ? '언팔로우' : '팔로우' }}
				</button>
			</div>
    </div>
  </div>
  <div v-else>
    <p>로딩 중이니 조금만 기다려 줄 수 있을꽉?</p>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const store = useMovieStore()
const user = ref(null)
const API_URL = store.API_URL
const route = useRoute()
const isFollowing = ref(false)
const followingCount = ref(0)
const followerCount = ref(0)

const isCurrentUser = computed(() => store.user && user.value && store.user.id === user.value.id)

const getUserInfo = async () => {
  try {
    const response = await axios.get(`${API_URL}/user/profile/${route.params.username}/`, {
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    user.value = response.data
    followingCount.value = user.value.followings.length
    followerCount.value = user.value.followers.length
    checkIfFollowing()
  } catch (error) {
    console.log(error.response)
  }
}

const checkIfFollowing = () => {
  if (store.user && user.value) {
    isFollowing.value = user.value.followers.some(follower => follower.id === store.user.id)
  }
}

const toggleFollow = async () => {
  try {
    const response = await axios.post(`${API_URL}/user/${user.value.id}/`, {}, {
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    if (response.data.status === 'followed') {
      isFollowing.value = true
      user.value.followers.push({ id: store.user.id })
      followerCount.value += 1
    } else if (response.data.status === 'unfollowed') {
      isFollowing.value = false
      user.value.followers = user.value.followers.filter(follower => follower.id !== store.user.id)
      followerCount.value -= 1
    }
  } catch (error) {
    console.log(error.response)
  }
}

onMounted(() => {
  getUserInfo()
})
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
</style>
