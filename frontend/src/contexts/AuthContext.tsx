import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import axios from 'axios'

const API_URL = (import.meta.env as any).VITE_API_URL || 'http://localhost:8000'

interface User {
  id: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => void
}

interface RegisterData {
  email: string
  password: string
  full_name: string
  phone?: string
  role?: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setUser({
      id: 'demo-user-id',
      email: 'demo@agreemate.com',
      full_name: 'Demo User',
      role: 'user',
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    })
    localStorage.setItem('token', 'mock-token-for-demo')
    setLoading(false)
  }, [])

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API_URL}/auth/me`)
      setUser(response.data)
    } catch (error) {
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const response = await axios.post(`${API_URL}/auth/login`, { email, password })
    const { access_token } = response.data
    
    localStorage.setItem('token', access_token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    await fetchUser()
  }

  const register = async (userData: RegisterData) => {
    await axios.post(`${API_URL}/auth/register`, userData)
    await login(userData.email, userData.password)
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
