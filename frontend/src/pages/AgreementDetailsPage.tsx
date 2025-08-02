import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { Separator } from '../components/ui/separator'
import { toast } from 'sonner'
import { 
  ArrowLeft, 
  FileText, 
  Download, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Stamp,
  PenTool,
  Users
} from 'lucide-react'
import axios from 'axios'

const API_URL = (import.meta.env as any).VITE_API_URL || 'http://localhost:8000'

interface Agreement {
  id: string
  title: string
  agreement_type: string
  status: string
  created_at: string
  updated_at: string
  template_data: Record<string, any>
  parties: Array<{ name: string; email: string; phone: string }>
  state: string
  stamp_duty_amount: number
  estamp_certificate_url?: string
  esign_document_url?: string
  final_document_url?: string
  activity_log: Array<{ action: string; timestamp: string; details?: any }>
}

interface ESignStatus {
  status: string
  session_id?: string
  agreement_id?: string
  pending_signers?: number
  signatures?: Array<{
    signer_name: string
    signed_at?: string
    status: string
  }>
  signed_document_url?: string
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

export function AgreementDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [agreement, setAgreement] = useState<Agreement | null>(null)
  const [esignStatus, setEsignStatus] = useState<ESignStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      fetchAgreement()
    }
  }, [id])

  const fetchAgreement = async () => {
    try {
      const response = await axios.get(`${API_URL}/agreements/${id}`)
      setAgreement(response.data)
    } catch (error: any) {
      toast.error('Failed to fetch agreement details')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleEStamp = async () => {
    if (!agreement) return
    
    setActionLoading('estamp')
    try {
      await axios.post(`${API_URL}/agreements/${agreement.id}/estamp`)
      toast.success('eStamp process initiated successfully!')
      await fetchAgreement()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to initiate eStamp process')
    } finally {
      setActionLoading(null)
    }
  }

  const handleESign = async () => {
    if (!agreement) return
    
    setActionLoading('esign')
    try {
      const response = await axios.post(`${API_URL}/agreements/${agreement.id}/esign`)
      setEsignStatus(response.data)
      toast.success('eSign process initiated successfully!')
      await fetchAgreement()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to initiate eSign process')
    } finally {
      setActionLoading(null)
    }
  }

  const checkESignStatus = async () => {
    if (!agreement || !esignStatus?.session_id) return
    
    try {
      const response = await axios.get(`${API_URL}/agreements/${agreement.id}/esign-status/${esignStatus.session_id}`)
      setEsignStatus(response.data)
      if (response.data.status === 'completed') {
        toast.success('All parties have signed the agreement!')
        await fetchAgreement()
      }
    } catch (error: any) {
      toast.error('Failed to check eSign status')
    }
  }

  const downloadPDF = async () => {
    if (!agreement) return
    
    setActionLoading('download')
    try {
      const response = await axios.get(`${API_URL}/agreements/${agreement.id}/pdf`, {
        responseType: 'blob'
      })
      
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${agreement.title}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      toast.success('PDF downloaded successfully!')
    } catch (error: any) {
      toast.error('Failed to download PDF')
    } finally {
      setActionLoading(null)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
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
          <p className="mt-4 text-gray-600">Loading agreement details...</p>
        </div>
      </div>
    )
  }

  if (!agreement) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Agreement not found</h2>
        <p className="text-gray-600 mb-6">The agreement you're looking for doesn't exist or you don't have access to it.</p>
        <Button onClick={() => navigate('/dashboard')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>
      </div>
    )
  }

  const statusInfo = getStatusConfig(agreement.status)
  const StatusIcon = statusInfo.icon

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <Button variant="ghost" onClick={() => navigate('/dashboard')} className="mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>
        
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{agreement.title}</h1>
            <p className="mt-2 text-gray-600 capitalize">
              {agreement.agreement_type.replace('_', ' ')} Agreement • {agreement.state}
            </p>
          </div>
          <Badge className={statusInfo.color}>
            <StatusIcon className="h-3 w-3 mr-1" />
            {statusInfo.label}
          </Badge>
        </div>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <FileText className="h-5 w-5 mr-2" />
                Agreement Details
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-500">Created:</span>
                  <p>{formatDate(agreement.created_at)}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Last Updated:</span>
                  <p>{formatDate(agreement.updated_at)}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">State:</span>
                  <p className="capitalize">{agreement.state.replace('_', ' ')}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Stamp Duty:</span>
                  <p>₹{agreement.stamp_duty_amount}</p>
                </div>
              </div>
              
              <Separator />
              
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Template Data</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                  {Object.entries(agreement.template_data).map(([key, value]) => (
                    <div key={key}>
                      <span className="font-medium text-gray-500 capitalize">
                        {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                      </span>
                      <p>{value as string}</p>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="h-5 w-5 mr-2" />
                Parties Involved
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {agreement.parties.map((party, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h4 className="font-medium text-gray-900">Party {index + 1}</h4>
                    <div className="mt-2 text-sm text-gray-600">
                      <p><span className="font-medium">Name:</span> {party.name}</p>
                      <p><span className="font-medium">Email:</span> {party.email}</p>
                      <p><span className="font-medium">Phone:</span> {party.phone}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {esignStatus && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PenTool className="h-5 w-5 mr-2" />
                  eSign Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Status:</span>
                    <Badge variant={esignStatus.status === 'completed' ? 'default' : 'secondary'}>
                      {esignStatus.status}
                    </Badge>
                  </div>
                  
                  {esignStatus.pending_signers !== undefined && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Pending Signers:</span>
                      <span className="text-sm">{esignStatus.pending_signers}</span>
                    </div>
                  )}
                  
                  {esignStatus.signatures && (
                    <div>
                      <h5 className="text-sm font-medium mb-2">Signature Status:</h5>
                      <div className="space-y-2">
                        {esignStatus.signatures.map((sig, index) => (
                          <div key={index} className="flex items-center justify-between text-sm">
                            <span>{sig.signer_name}</span>
                            <Badge variant={sig.status === 'completed' ? 'default' : 'secondary'}>
                              {sig.status}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {esignStatus.status === 'pending' && (
                    <Button onClick={checkESignStatus} variant="outline" size="sm">
                      Refresh Status
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Actions</CardTitle>
              <CardDescription>
                Manage your agreement workflow
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {agreement.status === 'draft' && (
                <Button 
                  onClick={handleEStamp} 
                  className="w-full"
                  disabled={actionLoading === 'estamp'}
                >
                  <Stamp className="h-4 w-4 mr-2" />
                  {actionLoading === 'estamp' ? 'Processing...' : 'Request eStamp'}
                </Button>
              )}
              
              {agreement.status === 'estamp_completed' && (
                <Button 
                  onClick={handleESign} 
                  className="w-full"
                  disabled={actionLoading === 'esign'}
                >
                  <PenTool className="h-4 w-4 mr-2" />
                  {actionLoading === 'esign' ? 'Initiating...' : 'Initiate eSign'}
                </Button>
              )}
              
              <Button 
                onClick={downloadPDF} 
                variant="outline" 
                className="w-full"
                disabled={actionLoading === 'download'}
              >
                <Download className="h-4 w-4 mr-2" />
                {actionLoading === 'download' ? 'Downloading...' : 'Download PDF'}
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Activity Log</CardTitle>
            </CardHeader>
            <CardContent>
              {agreement.activity_log.length > 0 ? (
                <div className="space-y-3">
                  {agreement.activity_log.map((activity, index) => (
                    <div key={index} className="text-sm">
                      <p className="font-medium">{activity.action}</p>
                      <p className="text-gray-500">{formatDate(activity.timestamp)}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">No activity recorded yet</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
