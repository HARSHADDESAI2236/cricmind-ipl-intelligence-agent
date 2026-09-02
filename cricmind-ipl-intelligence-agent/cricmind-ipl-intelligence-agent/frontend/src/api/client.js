import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('cricmind_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const sendChatMessage = (message, sessionId) =>
  client.post('/agent/chat', { message, sessionId }).then((r) => r.data)

export const getStandings = () => client.get('/standings').then((r) => r.data)
export const getMatches = () => client.get('/matches').then((r) => r.data)
export const getTeams = () => client.get('/teams').then((r) => r.data)
export const getPlayers = (search) =>
  client.get('/players', { params: { search } }).then((r) => r.data)
export const predictMatch = (payload) =>
  client.post('/predictions/match', payload).then((r) => r.data)
export const login = (username, password) =>
  client.post('/auth/login', { username, password }).then((r) => r.data)
export const register = (username, email, password) =>
  client.post('/auth/register', { username, email, password }).then((r) => r.data)

export default client
