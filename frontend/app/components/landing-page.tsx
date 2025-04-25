import { MainGraph } from "./main-graph"
import { SearchBar } from "./search-bar"
import { LearnMoreText } from "./learn-more"
import { DemoSection } from "./demo-section"
import { ApiAlert } from "./api-alert"

export default async function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <section className="h-screen">
        <div className="flex flex-col-reverse h-full lg:flex-row justify-center items-center text-center px-4">
          <div className="flex flex-col gap-4 animate-fade-up w-full max-w-[550px] mb-[50%] lg:mb-0">
            <div className="flex flex-col gap-2">
              <p className="font-bold text-5xl">Market Sentry</p>
              <p className="text-slate-500 text-xl">AI-powered financial companion</p>
            </div>
            <SearchBar />
          </div>
          <MainGraph />
        </div>
        <div className="flex w-full justify-center align-center">
          <LearnMoreText />
        </div>
      </section>
      <section>
        <div className="flex flex-col gap-16 px-4 py-24">
          <DemoSection
            header="Company Insights"
            description="Get valuable insights and summaries about top companies across the world. Discover trends and market sentiment from recent financial news and stories."
            redirect="/companies"
            videoUrl="https://player.vimeo.com/video/1040198203?autoplay=1&loop=1&muted=1&playsinline=1&controls=0&dnt=1"
          />
          <DemoSection
            header="AI Finance Assistant"
            description="Ask any finance-related question and receive valuable, real-time insights backed by reliable sources."
            redirect="/chat"
            videoUrl="https://player.vimeo.com/video/1040161670?autoplay=1&loop=1&muted=1&playsinline=1&controls=0&dnt=1"
          />
        </div>
      </section>
      <footer className="bg-background py-8 px-4 border-t">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <p className="text-muted-foreground mb-4 md:mb-0">&copy; 2024 All rights reserved.</p>
        </div>
      </footer>
      <ApiAlert />
    </div>
  )
}
