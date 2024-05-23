import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import MeetDetailView from '@/views/MeetDetailView.vue'
import CreateGroupView from '@/views/CreateGroupView.vue'
import { useMovieStore } from '@/stores/movie'
import MeetJoinView from '@/views/MeetJoinView.vue'
import MovieView from '@/views/MovieView.vue'
import MovieReviewEditView from '@/views/MovieReviewEditView.vue'
import UpdateMeetView from '@/views/UpdateMeetView.vue'
import Userprofile from '@/components/Userprofile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/meet_detail/:id',
      name: 'detail',
      component: MeetDetailView,
      props: true,
    },
    {
      path:'/meet_update/:id',
      name: 'update_meet',
      component: UpdateMeetView,
    },
    {
      path: '/joined_group',
      name: 'joined',
      component: MeetJoinView
    },
    {
      path: '/create_group',
      name: 'create',
      component: CreateGroupView
    },
    {
      path:'/meet/:meetId/movie/:movieId',
      name: 'movie',
      component: MovieView,
    },
    {
      path: '/:meetId/movie/:movieId/review/:reviewId/edit',
      name: 'reviewEdit',
      component: MovieReviewEditView,
    },
    {
      path: '/profile/:username',
      name: 'profile',
      component: Userprofile,
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})


router.beforeEach((to, from) => {
  const store = useMovieStore()
  if ((to.name === 'detail' || to.name === 'joined' || to.name === 'create' || to.name === 'movie' || to.name === 'update_meet') && (!store.isLogin)) {
    window.alert('🐣회원가입 또는 로그인해야합니덕🐣')
    return { name: 'home'}
  }
  if ((to.name === 'signup' || to.name === 'login') && (store.isLogin)) {
    window.alert('🐣이미 로그인 되어있덕🐣')
    return { name: 'home'}
  }
  if ((to.name === 'update_meet') && (store.user.id !== store.groupDetail.admin)) {
    window.alert('🐣모임 생성자만 수정할 수 있습니덕🐣')
    return { name: 'home'}
  }
})

export default router
