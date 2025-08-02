import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { toast } from 'sonner'
import { ArrowLeft } from 'lucide-react'

const agreementSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  agreement_type: z.string().min(1, 'Agreement type is required'),
  state: z.string().min(1, 'State is required'),
  stamp_duty_amount: z.number().min(0, 'Stamp duty amount must be positive').optional(),
})

type AgreementFormData = z.infer<typeof agreementSchema>

interface AgreementType {
  value: string
  label: string
  fields: string[]
}

interface State {
  value: string
  label: string
}

const agreementTypes: AgreementType[] = [
  {
    value: 'rental',
    label: 'Rental Agreement',
    fields: ['landlordName', 'landlordAddress', 'landlordPhone', 'landlordEmail', 'tenantName', 'tenantAddress', 'tenantPhone', 'tenantEmail', 'propertyAddress', 'propertyType', 'rentAmount', 'securityDeposit', 'startDate', 'endDate', 'lockInPeriod', 'rentDueDate', 'noticePeriod', 'witness1Name', 'witness1Address', 'witness2Name', 'witness2Address']
  },
  {
    value: 'employment',
    label: 'Employment Contract',
    fields: ['employerName', 'employerAddress', 'employerRegistration', 'employeeName', 'employeeAddress', 'employeePhone', 'employeeEmail', 'employeePAN', 'position', 'department', 'salary', 'basicSalary', 'allowances', 'bonusStructure', 'startDate', 'contractDate', 'employmentType', 'probationPeriod', 'workLocation', 'reportingManager', 'workingHours', 'leaveEntitlement', 'medicalInsurance', 'noticePeriod', 'witness1Name', 'witness1Address', 'witness2Name', 'witness2Address']
  },
  {
    value: 'service',
    label: 'Service Agreement',
    fields: ['serviceProviderName', 'serviceProviderAddress', 'clientName', 'clientAddress', 'serviceDescription', 'serviceAmount', 'startDate', 'endDate', 'paymentTerms']
  },
  {
    value: 'buyer_seller',
    label: 'Buyer-Seller Agreement',
    fields: ['sellerName', 'sellerAddress', 'sellerPhone', 'sellerEmail', 'buyerName', 'buyerAddress', 'buyerPhone', 'buyerEmail', 'propertyDescription', 'propertyAddress', 'salePrice', 'advanceAmount', 'balanceAmount', 'completionDate', 'agreementDate', 'witness1Name', 'witness1Address', 'witness2Name', 'witness2Address']
  },
  {
    value: 'nda',
    label: 'Non-Disclosure Agreement',
    fields: ['disclosingPartyName', 'disclosingPartyAddress', 'disclosingPartyEmail', 'receivingPartyName', 'receivingPartyAddress', 'receivingPartyEmail', 'purpose', 'termDuration', 'agreementDate']
  },
  {
    value: 'loan',
    label: 'Loan Agreement',
    fields: ['lenderName', 'lenderAddress', 'borrowerName', 'borrowerAddress', 'loanAmount', 'interestRate', 'startDate', 'endDate', 'repaymentDay', 'lateInterestRate', 'defaultInterestRate', 'agreementDate', 'witness1Name', 'witness1Address', 'witness2Name', 'witness2Address']
  }
]

const states: State[] = [
  { value: 'maharashtra', label: 'Maharashtra' },
  { value: 'delhi', label: 'Delhi' },
  { value: 'karnataka', label: 'Karnataka' },
  { value: 'tamil_nadu', label: 'Tamil Nadu' },
  { value: 'gujarat', label: 'Gujarat' },
  { value: 'rajasthan', label: 'Rajasthan' },
  { value: 'west_bengal', label: 'West Bengal' },
  { value: 'uttar_pradesh', label: 'Uttar Pradesh' }
]

export function CreateAgreementPage() {
  const navigate = useNavigate()
  const [selectedType, setSelectedType] = useState<AgreementType | null>(null)
  const [templateData, setTemplateData] = useState<Record<string, string>>({})
  const [parties, setParties] = useState([
    { name: '', email: '', phone: '' },
    { name: '', email: '', phone: '' }
  ])
  const [loading, setLoading] = useState(false)

  const {
    register,
    setValue,
    watch,
    formState: { errors }
  } = useForm<AgreementFormData>({
    resolver: zodResolver(agreementSchema)
  })

  const watchedType = watch('agreement_type')

  useEffect(() => {
    if (watchedType) {
      const type = agreementTypes.find(t => t.value === watchedType)
      setSelectedType(type || null)
      setTemplateData({})
    }
  }, [watchedType])

  const handleTemplateDataChange = (field: string, value: string) => {
    setTemplateData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handlePartyChange = (index: number, field: string, value: string) => {
    setParties(prev => prev.map((party, i) => 
      i === index ? { ...party, [field]: value } : party
    ))
  }

  const handleCreateAgreement = async () => {
    console.log('Button clicked - starting agreement creation')
    const formData = watch()
    
    if (!selectedType) {
      toast.error('Please select an agreement type')
      return
    }

    if (parties.some(party => !party.name || !party.email)) {
      toast.error('Please fill in all party details')
      return
    }

    if (!formData.title || !formData.agreement_type || !formData.state) {
      toast.error('Please fill in all required fields')
      return
    }

    setLoading(true)

    console.log('Creating agreement with data:', {
      ...formData,
      templateData,
      parties,
      selectedType: selectedType.value
    })

    await new Promise(resolve => setTimeout(resolve, 1500))
    
    toast.success('Agreement created successfully! Redirecting to dashboard...')
    
    setTimeout(() => {
      navigate('/dashboard')
    }, 1000)
    
    setLoading(false)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <Button variant="ghost" onClick={() => navigate('/dashboard')} className="mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">Create New Agreement</h1>
        <p className="mt-2 text-gray-600">Fill in the details to generate your legal document</p>
      </div>

      <div className="space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>
              Start by selecting the type of agreement and providing basic details
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="title">Agreement Title</Label>
              <Input
                id="title"
                {...register('title')}
                placeholder="Enter a descriptive title for your agreement"
              />
              {errors.title && (
                <p className="text-sm text-red-600 mt-1">{errors.title.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="agreement_type">Agreement Type</Label>
              <Select onValueChange={(value) => setValue('agreement_type', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select agreement type" />
                </SelectTrigger>
                <SelectContent>
                  {agreementTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.agreement_type && (
                <p className="text-sm text-red-600 mt-1">{errors.agreement_type.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="state">State</Label>
              <Select onValueChange={(value) => setValue('state', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select state" />
                </SelectTrigger>
                <SelectContent>
                  {states.map((state) => (
                    <SelectItem key={state.value} value={state.value}>
                      {state.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.state && (
                <p className="text-sm text-red-600 mt-1">{errors.state.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="stamp_duty_amount">Stamp Duty Amount (₹)</Label>
              <Input
                id="stamp_duty_amount"
                type="number"
                {...register('stamp_duty_amount', { valueAsNumber: true })}
                placeholder="100"
              />
              {errors.stamp_duty_amount && (
                <p className="text-sm text-red-600 mt-1">{errors.stamp_duty_amount.message}</p>
              )}
            </div>
          </CardContent>
        </Card>

        {selectedType && (
          <Card>
            <CardHeader>
              <CardTitle>Agreement Details</CardTitle>
              <CardDescription>
                Fill in the specific details for your {selectedType.label.toLowerCase()}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {selectedType.fields.map((field) => (
                <div key={field}>
                  <Label htmlFor={field}>
                    {field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                  </Label>
                  <Input
                    id={field}
                    value={templateData[field] || ''}
                    onChange={(e) => handleTemplateDataChange(field, e.target.value)}
                    placeholder={`Enter ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`}
                  />
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Parties Involved</CardTitle>
            <CardDescription>
              Add the details of all parties who will be signing this agreement
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {parties.map((party, index) => (
              <div key={index} className="border rounded-lg p-4">
                <h4 className="font-medium mb-3">Party {index + 1}</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor={`party-${index}-name`}>Full Name</Label>
                    <Input
                      id={`party-${index}-name`}
                      value={party.name}
                      onChange={(e) => handlePartyChange(index, 'name', e.target.value)}
                      placeholder="Enter full name"
                    />
                  </div>
                  <div>
                    <Label htmlFor={`party-${index}-email`}>Email</Label>
                    <Input
                      id={`party-${index}-email`}
                      type="email"
                      value={party.email}
                      onChange={(e) => handlePartyChange(index, 'email', e.target.value)}
                      placeholder="Enter email address"
                    />
                  </div>
                  <div>
                    <Label htmlFor={`party-${index}-phone`}>Phone</Label>
                    <Input
                      id={`party-${index}-phone`}
                      value={party.phone}
                      onChange={(e) => handlePartyChange(index, 'phone', e.target.value)}
                      placeholder="Enter phone number"
                    />
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <div className="flex justify-end space-x-4">
          <Button type="button" variant="outline" onClick={() => navigate('/dashboard')}>
            Cancel
          </Button>
          <Button type="button" disabled={loading} onClick={handleCreateAgreement}>
            {loading ? 'Creating...' : 'Create Agreement'}
          </Button>
        </div>
      </div>
    </div>
  )
}
