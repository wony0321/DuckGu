<template>
  <main>
    <div v-if="review" class="review-container">
      <p>리뷰 작성자 : {{ review.user.username }}</p>
      <div class="star-rating">
        <span>별점: &nbsp; </span>
        <MovieReviewStar :rate="review.rate" :editable="false" />
      </div>
      <p class="mt-3">리뷰: {{ review.content }}</p>
      <span v-if="store.user.id === review.user.id" class="button-group">
        <button @click="editReview" class="btn btn-orange">수정</button>
        <button @click="deleteReview" class="btn btn-orange">삭제</button>
      </span>
      <hr class="divider">
    </div>
  </main>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import MovieReviewStar from '@/components/MovieReviewStar.vue'

const router = useRouter()
const store = useMovieStore()
const review = ref(null)

const props = defineProps({
  reviewId: Number,
  meetId: Number,
  movie: Object
})

const emit = defineEmits(['reviewDeleted'])

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/duck9/movie/${props.movie.id}/review/${props.reviewId}`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      review.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
})

function editReview() {
  router.push({ name: 'reviewEdit', params: { meetId: props.meetId, movieId: props.movie.id, reviewId: props.reviewId } })
}

function deleteReview() {
  axios({
    method: 'delete',
    url: `${store.API_URL}/duck9/movie/${props.movie.id}/review/${props.reviewId}`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(() => {
      alert('리뷰가 삭제됐덕!🐣')
      emit('reviewDeleted')
    })
    .catch((err) => {
      console.log(err)
      alert('🦆꽉!!🦆: 리뷰 삭제에 실패했습니다.')
    })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

body {
  font-family: 'Gowun Dodum', sans-serif;
  background-color: #FFF9DB;
  margin: 0;
  padding: 0;
}

.review-container {
  padding: 10px;
}

.star-rating {
  display: flex;
  align-items: center;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end; /* 버튼을 오른쪽으로 정렬 */
}

.btn {
  padding: 7px;
  font-size: 16px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  width: 70px;
  transition: background-color 0.3s;
  align-self: flex-end;
}

.btn-orange {
  background-color: #FF8C00;
  color: white;
}

.btn-orange:hover {
  background-color: #FF7300;
}

.divider {
  border: 1px solid #FF8C00;
}
</style>
