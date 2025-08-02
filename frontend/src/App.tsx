import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { Navbar } from './components/Navbar'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { DashboardPage } from './pages/DashboardPage'
import { CreateAgreementPage } from './pages/CreateAgreementPage'
import { AgreementDetailsPage } from './pages/AgreementDetailsPage'
import './App.css'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }
  
  if (user) {
    return <Navigate to="/dashboard" replace />
  }
  
  return <>{children}</>
}

function AppContent() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          } />
          <Route path="/register" element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          } />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } />
          <Route path="/create-agreement" element={
            <ProtectedRoute>
              <CreateAgreementPage />
            </ProtectedRoute>
          } />
          <Route path="/agreement/:id" element={
            <ProtectedRoute>
              <AgreementDetailsPage />
            </ProtectedRoute>
          } />
        </Routes>
      </main>
      <Toaster />
    </div>
  )
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  )
}

export default App
