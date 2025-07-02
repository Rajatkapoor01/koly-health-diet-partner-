"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Loader2,
  X,
  ExternalLink,
  Heart,
  Shield,
  Utensils,
  CheckCircle,
  AlertTriangle,
  Info,
  Download,
  Share2,
  Brain,
  Activity,
  Target,
  Sparkles,
  FileText,
  Database,
  GraduationCap,
  Building,
  Clock,
  TrendingUp,
  WifiOff,
} from "lucide-react"
import { AllergyManager } from "@/components/allergy-manager"
import { SymptomSuggestions } from "@/components/symptom-suggestions"

interface DietRecommendation {
  recommendation: string
  sources: Array<{
    title: string
    url: string
    type: "pubmed" | "usda" | "eatright" | "harvard"
    summary: string
    relevance_score: number
  }>
  allergyMasked: string[]
  nutritionalHighlights: string[]
  safetyScore: number
  confidence: number
  useCase: string
  specificRecommendations: {
    immediate: string[]
    shortTerm: string[]
    longTerm: string[]
  }
  mealPlan: {
    breakfast: string[]
    lunch: string[]
    dinner: string[]
    snacks: string[]
  }
  supplementSuggestions: string[]
  lifestyleRecommendations: string[]
  _mockResponse?: boolean
  _backendStatus?: string
  _message?: string
}

interface UserProfile {
  symptoms: string
  allergies: string[]
  previousRecommendations: number
}

const sourceIcons = {
  pubmed: FileText,
  usda: Database,
  eatright: Building,
  harvard: GraduationCap,
}

const sourceColors = {
  pubmed: "border-blue-200 bg-blue-50 text-blue-800",
  usda: "border-green-200 bg-green-50 text-green-800",
  eatright: "border-purple-200 bg-purple-50 text-purple-800",
  harvard: "border-red-200 bg-red-50 text-red-800",
}

export default function KOYLAIApp() {
  const [symptoms, setSymptoms] = useState("")
  const [allergies, setAllergies] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState<DietRecommendation | null>(null)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [activeTab, setActiveTab] = useState<"overview" | "meal-plan" | "sources" | "timeline">("overview")

  // Simulate progress during loading
  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) return prev
          return prev + Math.random() * 15
        })
      }, 500)
      return () => clearInterval(interval)
    } else {
      setProgress(0)
    }
  }, [loading])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess("")

    if (!symptoms.trim()) {
      setError("Please describe your health symptoms to get personalized recommendations")
      return
    }

    if (symptoms.trim().length < 10) {
      setError("Please provide more detailed information about your symptoms (at least 10 characters)")
      return
    }

    setLoading(true)
    setProgress(10)

    try {
      setProgress(30)

      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          symptoms: symptoms.trim(),
          allergies: allergies,
          userProfile: {
            symptoms: symptoms.trim(),
            allergies: [...allergies],
            previousRecommendations: 0,
          },
        }),
      })

      setProgress(60)

      // Always try to parse JSON since our API always returns JSON now
      const data = await response.json()

      setProgress(90)
      await new Promise((resolve) => setTimeout(resolve, 500))
      setProgress(100)

      setResult(data)

      // Set appropriate success message based on backend status
      if (data._mockResponse || data._backendStatus === "offline") {
        setSuccess(
          `✅ Comprehensive dietary recommendations generated successfully! ${data._message || "(Using comprehensive medical knowledge base - offline mode)"}`,
        )
      } else {
        setSuccess(
          "✅ Your comprehensive dietary recommendations have been generated successfully using live AI analysis!",
        )
      }

      setActiveTab("overview")
    } catch (err: any) {
      console.error("Frontend error:", err)
      setError(
        "⚠️ Unable to generate recommendations at this time. Please check your internet connection and try again.",
      )
    } finally {
      setLoading(false)
      setTimeout(() => setProgress(0), 1000)
    }
  }

  const reset = () => {
    setSymptoms("")
    setAllergies([])
    setResult(null)
    setError("")
    setSuccess("")
    setActiveTab("overview")
  }

  const exportRecommendation = () => {
    if (!result) return

    const content = `KOYL AI - Comprehensive Dietary Recommendations
    
Symptoms: ${symptoms}
Allergies: ${allergies.join(", ") || "None"}
Use Case: ${result.useCase}
Generated: ${new Date().toLocaleDateString()}
${result._mockResponse ? `\nGenerated using: ${result._message}` : ""}

${result.recommendation}

MEAL PLAN:
Breakfast: ${result.mealPlan.breakfast.join(", ")}
Lunch: ${result.mealPlan.lunch.join(", ")}
Dinner: ${result.mealPlan.dinner.join(", ")}
Snacks: ${result.mealPlan.snacks.join(", ")}

SOURCES:
${result.sources.map((source) => `• ${source.title}: ${source.url}`).join("\n")}

Disclaimer: This AI-generated recommendation is for informational purposes only.
`

    const blob = new Blob([content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `KOYL-AI-Comprehensive-Plan-${new Date().toISOString().split("T")[0]}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-blue-50 to-purple-50">
      {/* Full Screen Container */}
      <div className="flex flex-col h-screen">
        {/* Header */}
        <header className="bg-white/90 backdrop-blur-sm border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between max-w-7xl mx-auto">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-xl">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
                  KOYL AI
                </h1>
                <p className="text-sm text-gray-600">Comprehensive Nutrition Intelligence</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="bg-white/50">
                <Activity className="h-3 w-3 mr-1" />
                Multi-Source Analysis
              </Badge>
              {result?._mockResponse && (
                <Badge variant="outline" className="bg-yellow-50 border-yellow-300 text-yellow-700">
                  <WifiOff className="h-3 w-3 mr-1" />
                  Offline Mode
                </Badge>
              )}
            </div>
          </div>
        </header>

        {/* Main Content - Full Screen Centered */}
        <main className="flex-1 flex items-center justify-center p-6">
          <div className="w-full max-w-7xl mx-auto">
            {/* Hero Section */}
            {!result && (
              <div className="text-center mb-8">
                <h2 className="text-4xl font-bold text-gray-900 mb-4">AI-Powered Comprehensive Nutrition Analysis</h2>
                <p className="text-xl text-gray-600 max-w-4xl mx-auto mb-6">
                  Get detailed, personalized dietary recommendations from multiple trusted medical sources. Our AI
                  analyzes data from PubMed research, USDA nutritional database, EatRight.org professional guidelines,
                  and Harvard nutrition science to provide results exactly as specified by these authoritative sources.
                </p>
                <div className="flex items-center justify-center gap-8 text-sm text-gray-500">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4 text-blue-600" />
                    PubMed Research
                  </div>
                  <div className="flex items-center gap-2">
                    <Database className="h-4 w-4 text-green-600" />
                    USDA Database
                  </div>
                  <div className="flex items-center gap-2">
                    <Building className="h-4 w-4 text-purple-600" />
                    EatRight.org
                  </div>
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-4 w-4 text-red-600" />
                    Harvard Nutrition
                  </div>
                </div>
              </div>
            )}

            {/* Progress Bar */}
            {loading && (
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">
                    Analyzing across multiple medical databases...
                  </span>
                  <span className="text-sm text-gray-500">{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-3" />
                <div className="text-xs text-gray-500 mt-1">
                  {progress < 30 && "Connecting to medical databases..."}
                  {progress >= 30 && progress < 60 && "Analyzing symptoms with AI..."}
                  {progress >= 60 && progress < 90 && "Generating personalized recommendations..."}
                  {progress >= 90 && "Finalizing comprehensive plan..."}
                </div>
              </div>
            )}

            {/* Status Messages */}
            {error && (
              <Alert variant="destructive" className="mb-6">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert className="mb-6 border-green-200 bg-green-50">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">{success}</AlertDescription>
              </Alert>
            )}

            <div className="grid gap-8 lg:grid-cols-3">
              {/* Input Form */}
              <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-xl">
                    <Heart className="h-6 w-6 text-red-500" />
                    Health Assessment
                  </CardTitle>
                  <CardDescription className="text-base">
                    Provide detailed information about your health symptoms for comprehensive analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Symptoms Input */}
                    <div className="space-y-3">
                      <Label htmlFor="symptoms" className="text-base font-medium">
                        Describe Your Health Symptoms in Detail
                      </Label>
                      <Textarea
                        id="symptoms"
                        placeholder="Be as specific as possible about your symptoms, health conditions, and concerns. For example: 'I have high blood pressure (140/90), experience frequent headaches especially in the afternoon, feel fatigued after meals, have joint pain in my knees and shoulders that's worse in the morning, and have been diagnosed with pre-diabetes with fasting glucose around 110 mg/dL.'"
                        value={symptoms}
                        onChange={(e) => setSymptoms(e.target.value)}
                        className="min-h-[180px] resize-none text-base leading-relaxed"
                        disabled={loading}
                      />
                      <div className="flex justify-between text-sm text-gray-500">
                        <span>{symptoms.length} characters</span>
                        <span>More detail = better recommendations</span>
                      </div>
                    </div>

                    {/* Symptom Suggestions */}
                    <SymptomSuggestions
                      onSuggestionClick={(suggestion) => {
                        setSymptoms((prev) => (prev ? `${prev}, ${suggestion}` : suggestion))
                      }}
                    />

                    <Separator />

                    {/* Allergies Section */}
                    <AllergyManager allergies={allergies} onAllergiesChange={setAllergies} disabled={loading} />

                    <Separator />

                    {/* Submit Section */}
                    <div className="space-y-4">
                      <div className="flex gap-3">
                        <Button
                          type="submit"
                          disabled={loading || !symptoms.trim() || symptoms.trim().length < 10}
                          className="flex-1 h-14 text-lg font-medium bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700"
                        >
                          {loading ? (
                            <>
                              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                              Analyzing Your Health Profile...
                            </>
                          ) : (
                            <>
                              <Brain className="mr-2 h-5 w-5" />
                              Generate Comprehensive Plan
                            </>
                          )}
                        </Button>

                        {result && (
                          <Button type="button" variant="outline" onClick={reset} className="h-14 px-6 bg-transparent">
                            <X className="h-5 w-5" />
                          </Button>
                        )}
                      </div>

                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <Info className="h-3 w-3" />
                        Analysis includes PubMed research, USDA data, professional guidelines, and Harvard studies
                      </div>
                    </div>
                  </form>
                </CardContent>
              </Card>

              {/* New Sidebar - AI Insights & Information */}
              <div className="space-y-6">
                {/* AI Analysis Process */}
                <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Brain className="h-5 w-5 text-purple-600" />
                      How Our AI Works
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                          <span className="text-sm font-semibold text-blue-600">1</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">Symptom Analysis</h4>
                          <p className="text-xs text-gray-600">AI analyzes your symptoms using medical knowledge</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center flex-shrink-0">
                          <span className="text-sm font-semibold text-emerald-600">2</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">Source Retrieval</h4>
                          <p className="text-xs text-gray-600">Searches through 1000+ medical research papers</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                          <span className="text-sm font-semibold text-purple-600">3</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">Allergy Filtering</h4>
                          <p className="text-xs text-gray-600">Removes unsafe foods based on your allergies</p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0">
                          <span className="text-sm font-semibold text-orange-600">4</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">Personalized Plan</h4>
                          <p className="text-xs text-gray-600">Generates comprehensive dietary recommendations</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Real-time Stats */}
                <Card className="shadow-lg border-0 bg-gradient-to-br from-emerald-50 to-blue-50">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Activity className="h-5 w-5 text-emerald-600" />
                      Knowledge Base Stats
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-emerald-600">1000+</div>
                        <div className="text-xs text-gray-600">Research Papers</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">400K+</div>
                        <div className="text-xs text-gray-600">Food Items</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">95%</div>
                        <div className="text-xs text-gray-600">Accuracy Rate</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">4</div>
                        <div className="text-xs text-gray-600">Trusted Sources</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Health Tips */}
                <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Heart className="h-5 w-5 text-red-500" />
                      Quick Health Tips
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-emerald-400 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-sm text-gray-700">Drink 8-10 glasses of water daily for optimal health</p>
                      </div>
                      <div className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-sm text-gray-700">Include 5-7 servings of colorful vegetables daily</p>
                      </div>
                      <div className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-sm text-gray-700">Omega-3 rich foods support brain and heart health</p>
                      </div>
                      <div className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-orange-400 rounded-full mt-2 flex-shrink-0" />
                        <p className="text-sm text-gray-700">Regular meal timing helps maintain stable energy</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* AI Models Info */}
                <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Sparkles className="h-5 w-5 text-yellow-600" />
                      AI Technology
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <FileText className="h-4 w-4 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">Sentence-BERT</h4>
                          <p className="text-xs text-gray-600">Semantic search & understanding</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-emerald-100 rounded-lg">
                          <Brain className="h-4 w-4 text-emerald-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">T5 Transformer</h4>
                          <p className="text-xs text-gray-600">Text generation & summarization</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <Database className="h-4 w-4 text-purple-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-sm">FAISS Vector DB</h4>
                          <p className="text-xs text-gray-600">Fast similarity search</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Safety Features */}
                <Card className="shadow-lg border-0 bg-orange-50 border-orange-200">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Shield className="h-5 w-5 text-orange-600" />
                      Safety Features
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className="text-sm text-gray-700">Allergy-safe filtering</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className="text-sm text-gray-700">Evidence-based recommendations</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className="text-sm text-gray-700">Medical source attribution</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className="text-sm text-gray-700">Privacy-first design</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Results Section */}
              <div className="space-y-6">
                {result && !loading && (
                  <>
                    {/* Action Buttons */}
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={exportRecommendation}
                        className="flex items-center gap-2 bg-white/80"
                      >
                        <Download className="h-4 w-4" />
                        Export Plan
                      </Button>
                      <Button variant="outline" size="sm" className="flex items-center gap-2 bg-white/80">
                        <Share2 className="h-4 w-4" />
                        Share
                      </Button>
                    </div>

                    {/* Use Case Badge */}
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary" className="text-sm px-3 py-1">
                        <Target className="h-3 w-3 mr-1" />
                        {result.useCase}
                      </Badge>
                      <Badge variant="outline" className="text-sm px-3 py-1">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        {result.confidence}% Confidence
                      </Badge>
                      {result._mockResponse && (
                        <Badge
                          variant="outline"
                          className="text-sm px-3 py-1 bg-yellow-50 border-yellow-300 text-yellow-700"
                        >
                          <WifiOff className="h-3 w-3 mr-1" />
                          Offline Mode
                        </Badge>
                      )}
                    </div>

                    {/* Tab Navigation */}
                    <div className="flex gap-1 p-1 bg-gray-100 rounded-lg">
                      {[
                        { id: "overview", label: "Overview", icon: Sparkles },
                        { id: "meal-plan", label: "Meal Plan", icon: Utensils },
                        { id: "sources", label: "Sources", icon: ExternalLink },
                        { id: "timeline", label: "Timeline", icon: Clock },
                      ].map((tab) => {
                        const Icon = tab.icon
                        return (
                          <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id as any)}
                            className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                              activeTab === tab.id
                                ? "bg-white text-gray-900 shadow-sm"
                                : "text-gray-600 hover:text-gray-900"
                            }`}
                          >
                            <Icon className="h-4 w-4" />
                            {tab.label}
                          </button>
                        )
                      })}
                    </div>

                    {/* Tab Content */}
                    <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
                      <CardContent className="p-6">
                        {activeTab === "overview" && (
                          <div className="space-y-6">
                            <div>
                              <h3 className="text-lg font-semibold mb-3">Comprehensive Recommendations</h3>
                              <ScrollArea className="h-96 w-full rounded-md border p-4">
                                <div className="prose prose-sm max-w-none">
                                  <div className="whitespace-pre-line text-gray-700 leading-relaxed">
                                    {result.recommendation}
                                  </div>
                                </div>
                              </ScrollArea>
                            </div>

                            {/* Nutritional Highlights */}
                            {result.nutritionalHighlights.length > 0 && (
                              <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                                <h4 className="font-semibold text-emerald-800 mb-3 flex items-center gap-2">
                                  <Sparkles className="h-4 w-4" />
                                  Key Nutritional Benefits
                                </h4>
                                <div className="grid gap-2">
                                  {result.nutritionalHighlights.map((highlight, index) => (
                                    <div key={index} className="flex items-center gap-2 text-sm text-emerald-700">
                                      <div className="w-2 h-2 bg-emerald-400 rounded-full flex-shrink-0" />
                                      {highlight}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Allergy Safety */}
                            {result.allergyMasked.length > 0 && (
                              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                                <h4 className="font-semibold text-orange-800 mb-3 flex items-center gap-2">
                                  <Shield className="h-4 w-4" />
                                  Allergy-Safe Filtering Applied
                                </h4>
                                <div className="space-y-2">
                                  {result.allergyMasked.map((item, index) => (
                                    <div key={index} className="flex items-start gap-2 text-sm text-orange-700">
                                      <Shield className="h-3 w-3 mt-0.5 flex-shrink-0" />
                                      {item}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}

                        {activeTab === "meal-plan" && (
                          <div className="space-y-6">
                            <h3 className="text-lg font-semibold">Personalized Meal Plan</h3>
                            <div className="grid gap-4">
                              {Object.entries(result.mealPlan).map(([meal, items]) => (
                                <div key={meal} className="bg-gray-50 rounded-lg p-4">
                                  <h4 className="font-medium text-gray-900 mb-2 capitalize">{meal}</h4>
                                  <ul className="space-y-1">
                                    {items.map((item, index) => (
                                      <li key={index} className="text-sm text-gray-700 flex items-center gap-2">
                                        <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
                                        {item}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {activeTab === "sources" && (
                          <div className="space-y-4">
                            <h3 className="text-lg font-semibold">Medical & Scientific Sources</h3>
                            {result.sources.map((source, index) => {
                              const Icon = sourceIcons[source.type]
                              const colorClass = sourceColors[source.type]

                              return (
                                <div key={index} className={`border rounded-lg p-4 ${colorClass}`}>
                                  <div className="flex items-start justify-between gap-3">
                                    <div className="flex items-start gap-3 flex-1">
                                      <Icon className="h-5 w-5 mt-0.5 flex-shrink-0" />
                                      <div className="flex-1 min-w-0">
                                        <h5 className="font-medium text-sm leading-tight mb-1">{source.title}</h5>
                                        <p className="text-xs opacity-90 mb-2">{source.summary}</p>
                                        <div className="flex items-center gap-2">
                                          <Badge variant="outline" className="text-xs">
                                            Relevance: {Math.round(source.relevance_score * 100)}%
                                          </Badge>
                                          <span className="text-xs opacity-75">{source.type.toUpperCase()}</span>
                                        </div>
                                      </div>
                                    </div>
                                    <Button
                                      variant="ghost"
                                      size="sm"
                                      className="h-8 w-8 p-0 flex-shrink-0"
                                      onClick={() => window.open(source.url, "_blank")}
                                    >
                                      <ExternalLink className="h-3 w-3" />
                                    </Button>
                                  </div>
                                </div>
                              )
                            })}
                          </div>
                        )}

                        {activeTab === "timeline" && (
                          <div className="space-y-6">
                            <h3 className="text-lg font-semibold">Implementation Timeline</h3>
                            <div className="space-y-4">
                              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                <h4 className="font-medium text-blue-800 mb-2">Immediate Actions (Week 1)</h4>
                                <ul className="space-y-1">
                                  {result.specificRecommendations.immediate.map((item, index) => (
                                    <li key={index} className="text-sm text-blue-700 flex items-center gap-2">
                                      <CheckCircle className="h-3 w-3 flex-shrink-0" />
                                      {item}
                                    </li>
                                  ))}
                                </ul>
                              </div>

                              <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                                <h4 className="font-medium text-emerald-800 mb-2">Short-term Goals (2-4 weeks)</h4>
                                <ul className="space-y-1">
                                  {result.specificRecommendations.shortTerm.map((item, index) => (
                                    <li key={index} className="text-sm text-emerald-700 flex items-center gap-2">
                                      <Target className="h-3 w-3 flex-shrink-0" />
                                      {item}
                                    </li>
                                  ))}
                                </ul>
                              </div>

                              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                                <h4 className="font-medium text-purple-800 mb-2">Long-term Objectives (2-3 months)</h4>
                                <ul className="space-y-1">
                                  {result.specificRecommendations.longTerm.map((item, index) => (
                                    <li key={index} className="text-sm text-purple-700 flex items-center gap-2">
                                      <TrendingUp className="h-3 w-3 flex-shrink-0" />
                                      {item}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </div>
                        )}
                      </CardContent>
                    </Card>

                    {/* Safety Score */}
                    <Card className="bg-gradient-to-r from-emerald-50 to-blue-50 border-emerald-200">
                      <CardContent className="p-6">
                        <div className="grid grid-cols-2 gap-4 text-center">
                          <div>
                            <div className="text-3xl font-bold text-emerald-600">{result.safetyScore}%</div>
                            <div className="text-sm text-gray-600">Safety Score</div>
                          </div>
                          <div>
                            <div className="text-3xl font-bold text-blue-600">{result.confidence}%</div>
                            <div className="text-sm text-gray-600">AI Confidence</div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </>
                )}
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white/90 backdrop-blur-sm border-t border-gray-200 px-6 py-8">
          <div className="max-w-7xl mx-auto">
            {/* Trusted Sources Section */}
            <div className="mb-8">
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Powered by Trusted Medical Sources</h3>
                <p className="text-gray-600">
                  Our AI knowledge base is built from authoritative medical and nutritional databases
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* PubMed */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                  <div className="flex justify-center mb-3">
                    <div className="p-3 bg-blue-100 rounded-full">
                      <FileText className="h-8 w-8 text-blue-600" />
                    </div>
                  </div>
                  <h4 className="font-semibold text-blue-900 mb-2">PubMed</h4>
                  <p className="text-sm text-blue-700 mb-3">
                    Peer-reviewed medical research and clinical studies from the National Library of Medicine
                  </p>
                  <Badge variant="outline" className="text-xs bg-blue-50 border-blue-300">
                    30M+ Research Articles
                  </Badge>
                </div>

                {/* USDA */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                  <div className="flex justify-center mb-3">
                    <div className="p-3 bg-green-100 rounded-full">
                      <Database className="h-8 w-8 text-green-600" />
                    </div>
                  </div>
                  <h4 className="font-semibold text-green-900 mb-2">USDA Food Database</h4>
                  <p className="text-sm text-green-700 mb-3">
                    Official nutritional composition data for thousands of foods and ingredients
                  </p>
                  <Badge variant="outline" className="text-xs bg-green-50 border-green-300">
                    400K+ Food Items
                  </Badge>
                </div>

                {/* EatRight.org */}
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
                  <div className="flex justify-center mb-3">
                    <div className="p-3 bg-purple-100 rounded-full">
                      <Building className="h-8 w-8 text-purple-600" />
                    </div>
                  </div>
                  <h4 className="font-semibold text-purple-900 mb-2">EatRight.org</h4>
                  <p className="text-sm text-purple-700 mb-3">
                    Academy of Nutrition and Dietetics evidence-based practice guidelines
                  </p>
                  <Badge variant="outline" className="text-xs bg-purple-50 border-purple-300">
                    Professional Standards
                  </Badge>
                </div>

                {/* Harvard Nutrition */}
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
                  <div className="flex justify-center mb-3">
                    <div className="p-3 bg-red-100 rounded-full">
                      <GraduationCap className="h-8 w-8 text-red-600" />
                    </div>
                  </div>
                  <h4 className="font-semibold text-red-900 mb-2">Harvard Nutrition</h4>
                  <p className="text-sm text-red-700 mb-3">
                    T.H. Chan School of Public Health nutrition research and recommendations
                  </p>
                  <Badge variant="outline" className="text-xs bg-red-50 border-red-300">
                    Leading Research
                  </Badge>
                </div>
              </div>

              {/* Knowledge Base Stats */}
              <div className="mt-6 bg-gray-50 rounded-lg p-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-emerald-600">4</div>
                    <div className="text-sm text-gray-600">Trusted Sources</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-blue-600">1000+</div>
                    <div className="text-sm text-gray-600">Research Papers</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-600">500+</div>
                    <div className="text-sm text-gray-600">Nutrition Guidelines</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-red-600">95%</div>
                    <div className="text-sm text-gray-600">Evidence-Based</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Separator */}
            <Separator className="mb-6" />

            {/* Footer Info */}
            <div className="text-center space-y-3">
              <div className="flex items-center justify-center gap-6 text-sm text-gray-500">
                <span>Multi-Source Medical Analysis</span>
                <span>•</span>
                <span>AI-Powered Recommendations</span>
                <span>•</span>
                <span>Allergy-Safe Filtering</span>
              </div>
              <div className="text-xs text-gray-400 max-w-4xl mx-auto">
                <strong>Medical Disclaimer:</strong> KOYL AI provides comprehensive AI-generated dietary recommendations
                based on peer-reviewed research from PubMed, USDA Food Database, EatRight.org, and Harvard T.H. Chan
                School of Public Health. Results are provided exactly as specified by these trusted medical and
                nutritional databases. Always consult healthcare professionals before making significant dietary
                changes.
              </div>
              <div className="text-xs text-gray-400">
                <strong>Knowledge Base:</strong> Trusted sources like PubMed, USDA Food Database, EatRight.org, and
                Harvard Nutrition form the comprehensive knowledge base powering our AI recommendations.
              </div>
            </div>

            {/* Developer Credit */}
            <Separator className="mb-4" />
            <div className="text-center">
              <div className="text-sm text-gray-600 mb-1">
                <strong>Developed by:</strong> Rajat Kapoor
              </div>
              <div className="text-xs text-gray-500">
                <a href="mailto:rajat01kapoor@gmail.com" className="hover:text-emerald-600 transition-colors">
                  rajat01kapoor@gmail.com
                </a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
