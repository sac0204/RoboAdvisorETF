import yfinance as yf
import pandas as pd
import streamlit as st
import numpy as np

ROI = {
    "Conservative": 0.0393,
    "Moderately Conservative": 0.044,
    "Balanced": 0.064,
    "Moderately Aggressive": 0.0955,
    "Aggressive": 0.1120,
    "Impact Investing": 0.0556
}

def questionnaire():
    st.title("RoboAdvisorETF")
    st.write("Group 6")

    questions = [
        "What's the primary goal for your investments?",
        "What's your experience with investments?",
        "What are your liquidity needs",
        "How long do you plan to keep your investment?",
        "If the value of your investments drops, what would you do?",
        "How often do you check your investment portfolio?",
        "What is your risk tolerance",
        "Please tell us about your income and expenses",
	    "What are your expected returns and expectations",
		"Are you an Impact investor? (Disclaimer: Impact investment portfolios might prioritize societal or environmental impact over high returns)"			
    ]

    options = [
        ["Capital preservation", "Regular income", "Moderate growth", "High growth", "Speculation"],
        ["Beginner", "Intermediate", "Advanced", "Expert"],
        ["Need access to funds immediately", "May need funds in the near future", "No immediate liquidity needs"],
        ["Less than a year", "1-3 years", "3-5 years", "5-10 years", "More than 10 years"],
        ["Sell all", "Sell some", "Do nothing", "Buy more"],
        ["Daily", "Weekly", "Monthly", "Quarterly", "Annually"],
        ["Extremely risk-averse", "Moderately risk-averse", "Comfortable with high-risk investments"],
		["Limited income, high expenses", "Moderate income, balanced expenses", "High income, low expenses"],
        ["Low return expectations", "Moderate return expectations", "High return expectations"],
        ["No", "Yes"]	
    ]

    scores = [
    [1, 2, 3, 4, 5],  
    [1, 3, 4, 5],
    [1, 3, 5],  
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2],  
    [1, 2, 3, 4, 5],  
    [1, 3, 5],  
    [1, 3, 5], 
    [1, 3, 5],  
    [0, 201]  
]

    total_score = 0
    all_answered = True

    for q, opts, sc in zip(questions, options, scores):
        answer = st.selectbox(q, [None] + opts)
        if answer:
            total_score += sc[opts.index(answer)]
        else:
            all_answered = False

    if all_answered:
        if total_score > 200:
            st.session_state.category = "Impact Investing"
        elif 10 <= total_score <= 13:
            st.session_state.category = "Conservative"
        elif 13 <= total_score <= 18:
            st.session_state.category = "Moderately Conservative"
        elif 18 <= total_score <= 30:
            st.session_state.category = "Balanced"
        elif 30 <= total_score <= 40:
            st.session_state.category = "Moderately Aggressive"
        else:
            st.session_state.category = "Aggressive"

        st.markdown(f"## **Your investment risk profile is: {st.session_state.category}**")

        st.session_state.age = st.number_input("Enter your age:", 18, 65, 30)
        st.session_state.end_age = st.number_input("The year of age until you want to invest:", st.session_state.age + 1, 100, st.session_state.age + 10)
        st.session_state.P = st.number_input("Enter your one-time deposit:", 100, 100000, 1000)
        st.session_state.PMT = st.number_input("Enter your monthly deposit:", 50, 5000, 100)

        if st.button("Show Financial Data"):
            show_financial_data(st.session_state.category)

# Tikker Mapping
ticker_info = {
    "VNQ": {
        "name": "Vanguard Real Estate ETF",
        "description": "This ETF tracks the performance of the MSCI US Investable Market Real Estate 25/50 Index."
    },
    "VOO": {
        "name": "Vanguard S&P 500 ETF",
        "description": "An ETF that tracks the S&P 500, providing exposure to large-cap U.S. stocks."
    },
    "GC=F": {
        "name": "Gold Futures",
        "description": "A standard futures contract for gold trading on the COMEX division of the New York Mercantile Exchange."
    },
    "PLTK": {
        "name": "Playtika Holding Corp.",
        "description": "A leading mobile gaming company."
    },
    "CSAN": {
        "name": "Cosan Limited",
        "description": "Operates in the energy, logistics, and natural resources industries."
    },
    "DHR": {
        "name": "Danaher Corporation",
        "description": "A science and technology innovator."
    },
    "LSXMA": {
        "name": "Liberty Media Corp Series A",
        "description": "Owns media and entertainment businesses."
    },
    "KMI": {
        "name": "Kinder Morgan",
        "description": "One of the largest energy infrastructure firms in the U.S."
    },
    "GRFS": {
        "name": "Grifols, S.A.",
        "description": "A global healthcare company."
    },
    "T": {
        "name": "AT&T Inc.",
        "description": "A multinational conglomerate holding company."
    },
    "TTE": {
        "name": "TotalEnergies SE",
        "description": "An integrated oil and gas company."
    },
    "NVS": {
        "name": "Novartis AG",
        "description": "A global healthcare company based in Switzerland."
    },
    "CHTR": {
        "name": "Charter Communications, Inc.",
        "description": "A leading broadband connectivity company."
    },
    "FXU": {
        "name": "First Trust Utilities AlphaDEX Fund",
        "description": "An ETF that seeks to track the StrataQuant Utilities Index."
    },
    "PUI": {
        "name": "Invesco DWA Utilities Momentum ETF",
        "description": "An ETF based on the Dorsey Wright Utilities Technical Leaders Index."
    },
    "IHF": {
        "name": "iShares U.S. Healthcare Providers ETF",
        "description": "Offers exposure to U.S. companies that provide health insurance, diagnostics, and specialized treatment."
    }
}

def display_etf_info(tickers):
    for ticker in tickers:
        st.subheader(ticker_info[ticker]['name'])
        st.write(ticker_info[ticker]['description'])




def show_financial_data(category):
    ticker_map = {
        "Conservative": ['VNQ','VOO','GC=F'],
        "Moderately Conservative": ["PLTK", "CSAN", "DHR"],
        "Balanced": ["LSXMA", "KMI", "GRFS"],
        "Moderately Aggressive": ["T", "TTE", "NVS"],
        "Aggressive": ["CHTR", "TTE", "NVS"],
        "Impact Investing": ["FXU", "PUI", "IHF"]
    }

    stock_data = {}
    for ticker in ticker_map[category]:
        stock_data[ticker] = yf.download(ticker, period="3y")['Close']

    df = pd.DataFrame(stock_data)
    
    
    
    # We use the pre-defined ROI for the category.
    mean_annual_return = ROI[category]

    t = st.session_state.end_age - st.session_state.age
    P = st.session_state.P
    PMT = st.session_state.PMT * 12  
    
    FV_lumpsum = P * (1 + mean_annual_return)**t
    FV_annuity = PMT * ((((1 + mean_annual_return)**t - 1) / mean_annual_return))
    FV = FV_lumpsum + FV_annuity

    yearly_FVs = [P]
    yearly_invested = [P]
    for i in range(1, t+1):
        yearly_FVs.append((yearly_FVs[-1] + PMT) * (1 + mean_annual_return))
        yearly_invested.append(yearly_invested[-1] + PMT)

    st.write(f"Expected Future Value of your investments after {t} years: ${FV:,.2f}")
    st.write(f"Average Yearly Return for the Portfolio: {mean_annual_return * 100:.2f}%")

    st.write("Yearly Expected Future Value of Investments:")
    st.line_chart(pd.DataFrame({'Invested Amount': yearly_invested, 'Future Value': yearly_FVs}), use_container_width=True)

    st.write("Portfolio stock return for the last 3 years :")
    st.line_chart(df, use_container_width=True, height=300)

   
    st.write("The portfolio exist of these ETFs")
    display_etf_info(ticker_map[category])

    if st.button("Back to Questions"):
        st.session_state.clear()
        questionnaire()

def main():
    if 'category' not in st.session_state:
        st.session_state.category = None
    questionnaire()

if __name__ == "__main__":
    main()
