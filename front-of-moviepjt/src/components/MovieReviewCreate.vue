<template>
  <div class="review-create-container">
    <h2 class="review-create-title">리뷰 작성</h2>
    <form @submit.prevent="submitReview" class="review-create-form">
      <div class="form-group">
        <label for="content" class="form-label">내용:</label>
        <textarea id="content" v-model="content" class="form-input" required></textarea>
      </div>
      <div class="form-group">
        <span>
          <label class="form-label">별점:</label>
        </span>
        <span>
          <MovieReviewStar :rate="rate" @update:rate="updateRate" />
        </span>
      </div>
      <button type="submit" class="form-submit">리뷰 제출</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import MovieReviewStar from './MovieReviewStar.vue'
import { useMovieStore } from '@/stores/movie'
// import { defineEmits } from 'vue'

const props = defineProps({
  movieId: Number
})

const emit = defineEmits(['review-submitted'])

const store = useMovieStore()
const content = ref('')
const rate = ref(0)

const computedRate = computed(() => {
  return rate.value
})

const updateRate = (newRate) => {
  rate.value = newRate
}

const submitReview = () => {
  axios({
    method: 'post',
    url: `${store.API_URL}/duck9/movie/${props.movieId}/review/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      content: content.value,
      rate: computedRate.value
    }
  })
    .then((res) => {
      console.log('리뷰 제출 성공:', res.data)
      emit('review-submitted')
      // 리뷰 제출 후, 초기화 또는 다른 작업 수행
      content.value = ''
      rate.value = 0
    })
    .catch((err) => {
      if (err.response && err.response.data) {
        const errors = err.response.data
        let errorMessage = '🦆꽉!!!🦆:'
        for (const key in errors) {
          errorMessage += `${errors[key]}`
        }
        window.alert(errorMessage)
      } else {
        console.error('리뷰 제출 실패:', err)
        window.alert('리뷰 제출에 실패했습니다. 다시 시도해주세요.')
      }
    })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  font-family: 'Gowun Dodum', sans-serif;
  background-color: #FFF9DB;
  margin: 0;
  padding: 0;
}

.review-create-container {
  width: 100%;
  max-width: 600px;
  margin: 20px auto;
}

.review-create-title {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #FF8C00;
  margin-bottom: 20px;
  margin-left: 3px;
}

.review-create-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-family: 'Gowun Dodum', sans-serif;
  font-size: 1rem;
  color: #141414;
  margin-bottom: 5px;
}

.form-input {
  font-family: 'Gowun Dodum', sans-serif;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #FF8C00;
  font-size: 1rem;
  resize: vertical;
}

.form-submit {
  font-family: 'Gowun Dodum', sans-serif;
  background-color: #fda336;
  color: white;
  border: none;
  padding: 7px;
  margin-top: 20px;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100px; /* 제출 버튼의 너비 조정 */
  align-self: flex-end;
}

.form-submit:hover {
  background-color: #FF7300;
}
</style>
