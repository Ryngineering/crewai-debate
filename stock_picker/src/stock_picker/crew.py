from dataclasses import Field
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from stock_picker.tools.PushNotification import PushNotificationTool


class TrendingCompany(BaseModel):
    """Model representing a trending company that is in the news for its stock performance"""

    name: str = Field(description="Name of the trending company")
    stock_symbol: Optional[str] = Field(
        description="Stock symbol of the trending company", default=None
    )
    reason_for_trending: str = Field(description="Reason why the company is trending")
    current_stock_price: Optional[float] = Field(
        description="Current stock price of the trending company", default=None
    )


class TrendingCompanyList(BaseModel):
    """List of trending companies that the StockPicker crew will analyze and report on"""

    companies: List[TrendingCompany] = Field(
        description="List of trending companies that the StockPicker crew will analyze and report on"
    )


class TrendingCompanyResearch(BaseModel):
    """Model representing the research findings for a trending company"""

    name: str = Field(description="Name of the trending company")
    stock_symbol: Optional[str] = Field(
        description="Stock symbol of the trending company", default=None
    )
    market_position: str = Field(description="Market position of the trending company")
    future_outlook: str = Field(description="Future outlook for the trending company")
    investment_potential: str = Field(
        description="Investment potential and suitability of the trending company"
    )
    reason_for_trending: str = Field(description="Reason why the company is trending")
    current_stock_price: Optional[float] = Field(
        description="Current stock price of the trending company", default=None
    )
    analysis_summary: str = Field(
        description="Summary of the analysis for the trending company"
    )
    recommendation: str = Field(
        description="Investment recommendation for the trending company based on the analysis"
    )


class TrendingCompanyResearchList(BaseModel):
    """List of research findings for trending companies"""

    research_findings: List[TrendingCompanyResearch] = Field(
        description="List of research findings for trending companies"
    )


@CrewBase
class StockPicker:
    """StockPicker crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def trending_company_finder(self) -> Agent:
        """Agent responsible for researching trending companies and analyzing their stock performance"""
        return Agent(
            config=self.agents_config["trending_company_finder"],
            tools=[SerperDevTool()],
        )

    @agent
    def financial_researcher(self) -> Agent:
        """Agent responsible for analyzing the financial performance of trending companies and providing investment recommendations"""
        return Agent(
            config=self.agents_config["financial_researcher"], tools=[SerperDevTool()]
        )

    @agent
    def stock_picker(self) -> Agent:
        """Agent responsible for picking stocks based on the research and analysis provided by the research and financial analyst agents"""
        return Agent(
            config=self.agents_config["stock_picker"], tools=[PushNotificationTool()]
        )

    @task
    def find_trending_companies(self) -> Task:
        """Task to find trending companies that are in the news for their stock performance"""
        # Implementation to find trending companies and return a list of TrendingCompany objects
        return Task(
            config=self.tasks_config["find_trending_companies"],
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        """Task to research the trending companies and analyze their stock performance"""
        # Implementation to research the trending companies and return a list of TrendingCompanyResearch objects
        return Task(
            config=self.tasks_config["research_trending_companies"],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_stocks(self) -> Task:
        """Task to pick stocks based on the research and analysis provided by the research and financial analyst agents"""
        # Implementation to pick stocks based on the research and analysis and return a list of stock symbols or investment recommendations
        return Task(config=self.tasks_config["pick_best_stocks"])

    @crew
    def crew(self) -> Crew:
        """Crew to orchestrate the tasks of finding trending companies, researching them, and picking stocks based on the analysis"""
        manager = Agent(config=self.agents_config["manager"], allow_delegation=True)

        return Crew(
            name="StockPickerCrew",
            manager_agent=manager,
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
        )
