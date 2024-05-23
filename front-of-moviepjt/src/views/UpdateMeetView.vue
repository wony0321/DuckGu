<template>
  <main class="edit-meet-container">
  <h1 class="edit-meet-title">둥지 수정하기</h1>
  <form @submit.prevent="updateMeet" class="edit-meet-form">
    <div class="form-group">
      <label for="name" class="form-label">둥지 이름 뭐로 바꿀꽉?</label>
      <input type="text" id="name" v-model="name" class="form-input" />
    </div>

    <div class="form-group">
      <label for="genre" class="form-label">좋아하는 장르도 바꿀꽉? (다 골라봙)</label>
      <select id="genre" multiple class="form-input">
        <option
          v-for="genre in [...new Set(keywords.map(keyword => keyword.genre).filter(genre => genre))]"
          :key="genre"
          :value="genre"
          :class="{ selected: selectedGenres.includes(genre) }"
          @click="toggleSelection(selectedGenres, genre)"
          style="border-radius: 5px; padding: 3px;"
        >
          {{ genre }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="origin_country" class="form-label">좋아하는 국가도 바꿀꽉? (다 골라봙)</label>
      <select id="origin_country" multiple class="form-input">
        <option
          v-for="country in [...new Set(keywords.map(keyword => keyword.origin_country).filter(country => country))]"
          :key="country"
          :value="country"
          :class="{ selected: selectedCountries.includes(country) }"
          @click="toggleSelection(selectedCountries, country)"
          style="border-radius: 5px; padding: 3px;"
        >
          {{ country }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="era" class="form-label">좋아하는 시대도 바꿀꽉? (다 골라봙)</label>
      <select id="era" multiple class="form-input">
        <option
          v-for="era in [...new Set(keywords.map(keyword => keyword.era).filter(era => era))]"
          :key="era"
          :value="era"
          :class="{ selected: selectedEras.includes(era) }"
          @click="toggleSelection(selectedEras, era)"
          style="border-radius: 5px; padding: 3px;"
        >
          {{ era }}
        </option>
      </select>
    </div>

    <input type="submit" class="form-submit" value="모임 수정하기">
  </form>
</main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter, useRoute } from 'vue-router'

const store = useMovieStore()
const router = useRouter()
const route = useRoute()

const name = ref('')
const keywords = ref(store.keywords)
const selectedGenres = ref([])
const selectedCountries = ref([])
const selectedEras = ref([])

const meetId = route.params.id

const fetchMeetData = async () => {
await store.getGroupDetail(meetId)
const groupDetail = store.groupDetail

name.value = groupDetail.name

// 기존 키워드 설정
groupDetail.keywords.forEach(keywordId => {
  const keyword = keywords.value.find(keyword => keyword.id === keywordId)
  if (keyword) {
    if (keyword.genre && !selectedGenres.value.includes(keyword.genre)) {
      selectedGenres.value.push(keyword.genre)
    }
    if (keyword.origin_country && !selectedCountries.value.includes(keyword.origin_country)) {
      selectedCountries.value.push(keyword.origin_country)
    }
    if (keyword.era && !selectedEras.value.includes(keyword.era)) {
      selectedEras.value.push(keyword.era)
    }
  }
})
}

onMounted(() => {
fetchMeetData()
})

const toggleSelection = (selectedList, value) => {
const index = selectedList.indexOf(value)
if (index === -1) {
  selectedList.push(value)
} else {
  selectedList.splice(index, 1)
}
}

const updateMeet = function () {
const selectedKeywords = keywords.value.filter(keyword => 
  selectedGenres.value.includes(keyword.genre) || 
  selectedCountries.value.includes(keyword.origin_country) || 
  selectedEras.value.includes(keyword.era)
).map(keyword => keyword.id)

const payload = {
  name: name.value,
  keywords: selectedKeywords
}

store.meetUpdateAndDelete(meetId, payload, 'put')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  background-color: #FFF9DB; /* 연한 노란색 배경 */
  font-family: 'Gowun Dodum', sans-serif; /* 귀여운 글꼴 */
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.edit-meet-container {
  font-family: 'Gowun Dodum', sans-serif;
  width: 90%;
  max-width: 500px;
  text-align: center;
  background: #FFF2B2; /* 연한 주황색 배경 */
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.edit-meet-title {
  font-family: 'Nanum Gothic', sans-serif;
  color: #FF8C00; /* 주황색 텍스트 */
  font-size: 2rem;
  margin-bottom: 20px;
  text-align: center;
  font-weight: 900;
}

.edit-meet-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-label {
  margin-bottom: 5px;
  color: #141414; /* 주황색 텍스트 */
  text-align: center;
}

.form-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #FF8C00;
  font-size: 1rem;
}

.form-submit {
  background-color: #FF8C00;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 15px;
}

.form-submit:hover {
  background-color: #FF7300;
}

option.selected {
  background-color: rgb(255, 236, 175);
}
</style>
