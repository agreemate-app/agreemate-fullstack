import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { Plus, FileText, Clock, CheckCircle, AlertCircle } from 'lucide-react'

interface Agreement {
  id: string
  title: string
  agreement_type: string
  status: string
  created_at: string
  updated_at: string
}

const statusConfig = {
  draft: { label: 'Draft', color: 'bg-gray-100 text-gray-800', icon: FileText },
  estamp_pending: { label: 'eStamp Pending', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  estamp_completed: { label: 'eStamp Complete', color: 'bg-blue-100 text-blue-800', icon: CheckCircle },
  esign_pending: { label: 'eSign Pending', color: 'bg-orange-100 text-orange-800', icon: Clock },
  esign_completed: { label: 'eSign Complete', color: 'bg-green-100 text-green-800', icon: CheckCircle },
  completed: { label: 'Completed', color: 'bg-green-100 text-green-800', icon: CheckCircle },
  failed: { label: 'Failed', color: 'bg-red-100 text-red-800', icon: AlertCircle }
}

export function DashboardPage() {
  const { user } = useAuth()
  const [agreements, setAgreements] = useState<Agreement[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const mockAgreements: Agreement[] = [
      {
        id: 'agreement-1',
        title: 'Rental Agreement - Downtown Apartment',
        agreement_type: 'rental',
        status: 'completed',
        created_at: '2025-07-15T10:30:00Z',
        updated_at: '2025-07-20T14:45:00Z'
      },
      {
        id: 'agreement-2', 
        title: 'Employment Contract - Software Developer',
        agreement_type: 'employment',
        status: 'esign_pending',
        created_at: '2025-07-25T09:15:00Z',
        updated_at: '2025-07-25T09:15:00Z'
      },
      {
        id: 'agreement-3',
        title: 'Service Agreement - Web Development',
        agreement_type: 'service',
        status: 'estamp_completed',
        created_at: '2025-08-01T16:20:00Z',
        updated_at: '2025-08-02T11:30:00Z'
      }
    ]
    
    setTimeout(() => {
      setAgreements(mockAgreements)
      setLoading(false)
    }, 500) // Simulate loading time
  }, [])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getStatusConfig = (status: string) => {
    return statusConfig[status as keyof typeof statusConfig] || statusConfig.draft
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your agreements...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.full_name}</h1>
        <p className="mt-2 text-gray-600">Manage your legal documents and agreements</p>
      </div>

      <div className="mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Your Agreements</h2>
          <Button asChild>
            <Link to="/create-agreement">
              <Plus className="h-4 w-4 mr-2" />
              Create New Agreement
            </Link>
          </Button>
        </div>

        {agreements.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No agreements yet</h3>
              <p className="text-gray-600 mb-6">Get started by creating your first legal document</p>
              <Button asChild>
                <Link to="/create-agreement">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Agreement
                </Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {agreements.map((agreement) => {
              const statusInfo = getStatusConfig(agreement.status)
              const StatusIcon = statusInfo.icon
              
              return (
                <Card key={agreement.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg">{agreement.title}</CardTitle>
                        <CardDescription className="capitalize">
                          {agreement.agreement_type.replace('_', ' ')} Agreement
                        </CardDescription>
                      </div>
                      <Badge className={statusInfo.color}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {statusInfo.label}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm text-gray-600">
                      <p>Created: {formatDate(agreement.created_at)}</p>
                      <p>Updated: {formatDate(agreement.updated_at)}</p>
                    </div>
                    <div className="mt-4">
                      <Button asChild variant="outline" className="w-full">
                        <Link to={`/agreement/${agreement.id}`}>
                          View Details
                        </Link>
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
