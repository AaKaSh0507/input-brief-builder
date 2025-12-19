import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import BriefEditor from '../views/BriefEditor.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Dashboard - GPJ Input Brief Assistant' }
  },
  {
    path: '/brief/new',
    name: 'NewBrief',
    component: BriefEditor,
    meta: { title: 'New Brief' }
  },
  {
    path: '/brief/:id',
    name: 'EditBrief',
    component: BriefEditor,
    meta: { title: 'Edit Brief' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'GPJ Input Brief Assistant'
  next()
})

export default router
