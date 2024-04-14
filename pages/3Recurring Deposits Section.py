import streamlit as st
import math
import pandas as pd
import altair as alt

if 'rd_df' not in st.session_state:
    st.session_state.rd_df = pd.DataFrame( [] )
    st.session_state.rdinterest = 0.0
    st.session_state.rdinstalment = 0.0
comprd_mapping = {
    "Daily": 360,
    "Monthly": 12,
    "Quarterly": 4,
    "Half Yearly": 2,
    "Yearly": 1
}

freqrd_mapping = {
    "Days": 360,
    "Months": 12,
    "Quarters": 4,
    "Half Years": 2,
    "Years": 1
}

headrd_mapping = {
    "Daily": "Days",
    "Monthly": "Months",
    "Quarterly": "Quarters",
    "Half Yearly": "Half Years",
    "Yearly": "Years"
}

def showrdaccount():
    reportarr = []
    intrate = st.session_state.rd_rate / 100
    period = st.session_state.rd_term
    maturity = st.session_state.rd_matu
    instal = st.session_state.rd_inst
    yearlycompoundings = comprd_mapping.get(st.session_state.rd_comp)
    yearlyinstalments = freqrd_mapping.get(st.session_state.rd_freq)
    m = 0.0
    roundby = 2
    total1 = 0.0
    total2 = 0.0
    if yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        head1 = st.session_state.rd_freq
        counter = 1
        count1 = 1
        balance = 0.0
        totint = 0
        totinst = 0
        product = 0
        interest = 0
        while counter <= period:
            product = product + balance + instal
            totinst = totinst + instal
            if math.fmod(counter,yearlyinstalments/yearlycompoundings) == 0:
                interest = round(product * m,2)
                totint = interest + totint
                product = 0.0
            if counter > (fulcomp / yearlycompoundings * yearlyinstalments):
                product = 0
                while count1 <= balacomp:
                    product = product + balance + instal
                    if counter == period:
                        interest = round(product * m,2)
                        totint = interest + totint
                        product = 0
                        reportarr.append(
                            {
                                head1: counter,
                                'Opening Balance': round(balance, roundby),
                                'Instalment': round(instal, roundby),
                                'Total': round(balance + instal, roundby),
                                'Interest': round(interest, roundby),
                                'Closing Balance': round(balance + interest + instal, roundby)
                            }    
                        )        
                    balance = balance + interest + instal
                    count1 = count1 + 1
                    counter = counter + 1
                    interest = 0.0
            if counter <= (fulcomp / yearlycompoundings * yearlyinstalments):
                reportarr.append(
                    {
                        head1: counter,
                        'Opening Balance': round(balance, roundby),
                        'Instalment': round(instal, roundby),
                        'Total': round(balance + instal, roundby),
                        'Interest': round(interest, roundby),
                        'Closing Balance': round(balance + interest + instal, roundby)
                    }    
                )        
                balance = balance + interest + instal
                counter = counter + 1
                interest = 0.0
        total1 = 0.0
        total2 = 0.0
        for i in reportarr:
            total1 = total1 + i["Instalment"]
            total2 = total2 + i["Interest"]
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings  
        n = (yearlycompoundings/yearlyinstalments)
        head1 = headrd_mapping.get(st.session_state.rd_comp)
        counter = 1
        count1 = 1
        instal1 = 0.0
        balance = 0.0
        totint = 0.0
        totinst = 0.0
        product = 0.0
        interest = 0.0
        comcount = 1
        inscount = 1
        while counter <= period * yearlycompoundings/yearlyinstalments:
            if inscount == n or counter == 1:
                instal1 = instal
                totinst = totinst + instal1
                inscount = 0
            else:
                instal1 = 0.0
            product = balance + product + instal1
            interest = round(product * m,2)
            totint = totint + interest
            product = 0.0
            reportarr.append(
                {
                    head1: counter,
                    'Opening Balance': round(balance, roundby),
                    'Instalment': round(instal1, roundby),
                    'Total': round(balance + instal1, roundby),
                    'Interest': round(interest, roundby),
                    'Closing Balance': round(balance + interest + instal1, roundby)
                }    
            )        
            balance = balance + interest + instal1
            counter = counter + 1
            inscount = inscount + 1
            interest = 0
        total1 = 0.0
        total2 = 0.0
        for i in reportarr:
            total1 = total1 + i["Instalment"]
            total2 = total2 + i["Interest"]
    st.session_state.rd_df = pd.DataFrame( reportarr )
    st.session_state.rdinstalment = round(total1, roundby)
    st.session_state.rdinterest = round(total2, roundby)    


def rd_inst_calc():
    intrate = st.session_state.rd_rate / 100
    period = st.session_state.rd_term
    maturity = st.session_state.rd_matu
    instal = 0.0
    yearlycompoundings = comprd_mapping.get(st.session_state.rd_comp)
    yearlyinstalments = freqrd_mapping.get(st.session_state.rd_freq)
    m = 0.0
    if maturity == 0.0 or intrate == 0.0 or period == 0.0:
        st.error("You have to enter Interest Rate, Term of the Deposit and Maturity Value to find out the Instalment Amount.")
    elif yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        total1 = 0.0
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        if fulcomp > 0:
            n = yearlyinstalments / yearlycompoundings
            l = n  + (((n * (n + 1)) / 2) * (intrate / yearlyinstalments))
            total1 = l
            for i in range(2, fulcomp+1):
                total1 = (total1 * (1 + (intrate / yearlycompoundings))) + l
        total1 = (total1 * (1 + ((intrate / yearlyinstalments) * balacomp)))+ balacomp + (((balacomp * (balacomp + 1)) / 2) * (intrate / yearlyinstalments))
        instal = maturity / total1
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings
        total1 = (1+m)**(yearlycompoundings / yearlyinstalments)
        for i in range(2, int(period)+1):
            total1 = total1 + 1
            total1 = (total1 * (1+m)**(yearlycompoundings / yearlyinstalments))
        instal = maturity / total1
    st.session_state.rd_inst = instal
    showrdaccount()
    
def rd_term_calc():
    intrate = st.session_state.rd_rate / 100
    period = 0
    maturity = st.session_state.rd_matu
    instal = st.session_state.rd_inst
    yearlycompoundings = comprd_mapping.get(st.session_state.rd_comp)
    yearlyinstalments = freqrd_mapping.get(st.session_state.rd_freq)
    m = 0.0
    if instal == 0.0 or intrate == 0.0 or maturity == 0.0:
        st.error("You have to enter Instalment Amount, Interest Rate and the Maturity Value to find out the Term of Deposit.")
    elif instal >= maturity:
        st.error("Maturity value MUST be greater than instalment amount!")
    elif yearlyinstalments >= yearlycompoundings:
        period = 1
        crossed = False
        m = intrate / yearlyinstalments
        n = yearlyinstalments / yearlycompoundings
        while not crossed:
            fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
            balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
            total1 = 0.0
            if fulcomp > 0:
                l = n  + (((n * (n + 1)) / 2) * (intrate / yearlyinstalments))
                total1 = l
                for i in range(2, fulcomp+1):
                    total1 = (total1 * (1 + (intrate / yearlycompoundings))) + l
            total1 = (total1 * (1 + ((intrate / yearlyinstalments) * balacomp)))+ balacomp + (((balacomp * (balacomp + 1)) / 2) * (intrate / yearlyinstalments))
            if total1 * instal >= maturity:
                crossed = True
            else:
                period = period + 1
    elif yearlyinstalments < yearlycompoundings:
        period = 1
        crossed = False
        x = (yearlycompoundings / yearlyinstalments)
        while not crossed:
            m = intrate / yearlycompoundings
            total1 = (1+m)**x
            for i in range(2, int(period) + 1 ):
                total1 = total1 + 1
                total1 = (total1 * (1+m)** x)
            if total1 * instal >= maturity:
                crossed = True
            else:
                period = period + 1
    st.session_state.rd_term = round( period )
    showrdaccount()
    

def rd_matu_calc():
    intrate = st.session_state.rd_rate / 100
    period = st.session_state.rd_term
    maturity = 0.0
    instal = st.session_state.rd_inst
    yearlycompoundings = comprd_mapping.get(st.session_state.rd_comp)
    yearlyinstalments = freqrd_mapping.get(st.session_state.rd_freq)
    m = 0.0
    if instal == 0.0 or intrate == 0.0 or period == 0.0:
        st.error("You have to enter Instalment Amount, Interest Rate and the Term of the Deposit to find out the Maturity Value.")
    elif yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        total1 = 0.0
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        if fulcomp > 0:
            n = yearlyinstalments / yearlycompoundings
            l = n  + (((n * (n + 1)) / 2) * (intrate / yearlyinstalments))
            total1 = l
            for i in range( 2, fulcomp + 1):
                total1 = (total1 * (1 + (intrate / yearlycompoundings))) + l
        total1 = (total1 * (1 + ((intrate / yearlyinstalments) * balacomp)))+ balacomp + (((balacomp * (balacomp + 1)) / 2) * (intrate / yearlyinstalments))
        maturity = total1 * instal
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings
        total1 = (1+m)**(yearlycompoundings / yearlyinstalments)
        for i in range(2, int(period)+1):
            total1 = total1 + 1
            total1 = (total1 * (1+m)**(yearlycompoundings / yearlyinstalments))
        maturity = total1 * instal
    st.session_state.rd_matu = maturity
    showrdaccount()
    

def rd_rate_calc():
    intrate = 0.0
    period = st.session_state.rd_term
    maturity = st.session_state.rd_matu
    instal = st.session_state.rd_inst
    yearlycompoundings = comprd_mapping.get(st.session_state.rd_comp)
    yearlyinstalments = freqrd_mapping.get(st.session_state.rd_freq)
    m = 0.0
    if maturity == 0.0 or instal == 0.0 or period == 0.0:
        st.error("You have to enter Instalment Amount, Term of the Deposit and the Maturity Value to find out the Rate of Interest.")
    elif instal * period >= maturity:
        st.error("Maturity value MUST be greater than amount invested.")
    elif yearlyinstalments >= yearlycompoundings:
        intrate = 0.00001
        crossed = False
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        n = yearlyinstalments / yearlycompoundings
        while not crossed:
            m = intrate / yearlyinstalments
            total1 = 0.0
            if fulcomp > 0:
                l = n  + (((n * (n + 1)) / 2) * (intrate / yearlyinstalments))
                total1 = l
                for i in range( 2, fulcomp + 1):
                    total1 = (total1 * (1 + (intrate / yearlycompoundings))) + l
            total1 = (total1 * (1 + ((intrate / yearlyinstalments) * balacomp)))+ balacomp + (((balacomp * (balacomp + 1)) / 2) * (intrate / yearlyinstalments))
            if total1 * instal >= maturity:
                crossed = True
            else:
                if maturity - (total1 * instal) > 1000:
                    intrate = intrate + 0.0001
                else:
                    intrate = intrate + 0.00001
    elif yearlyinstalments < yearlycompoundings:
        intrate = 0.00001
        crossed = False
        x = (yearlycompoundings / yearlyinstalments)
        while not crossed:
            m = intrate / yearlycompoundings
            total1 = (1+m)**x
            for i in range(2, int(period) + 1):
                total1 = total1 + 1
                total1 = (total1 * (1+m)**x)
            if total1 * instal >= maturity:
                crossed = True
            else:
                if maturity - (total1 * instal) > 1000:
                    intrate = intrate + 0.0001
                else:
                    intrate = intrate + 0.00001
    st.session_state.rd_rate = intrate * 100
    showrdaccount()

[image, title, empty] = st.columns([0.25, 0.25, 0.5])
with image:
    st.image("./pages/RecurringDepositSection.jpg")
with title:
    st.write("# :green[Recurring Deposits Section]")
[col1, col2] = st.columns([0.5, 0.5])
with col1:
    st.button("Interest Compounding", disabled=True, use_container_width=True)
    st.selectbox("Compounding",("Daily", "Monthly", "Quarterly","Half Yearly","Yearly"), label_visibility="collapsed", key="rd_comp")
    st.button("Instalment Frequency", disabled=True, use_container_width=True)
    st.selectbox("Frequency",("Days", "Months", "Quarters","Half Years","Years"), label_visibility="collapsed", key="rd_freq")
    st.button("Deposit Amount", on_click=rd_inst_calc, use_container_width=True)
    st.number_input("Deposit", min_value=0.0, step=1000.0, label_visibility="collapsed", key="rd_inst")
    st.button("Interest Rate (% p.a.)", on_click=rd_rate_calc, use_container_width=True)
    st.number_input("Interest Rate", min_value=0.0, step=0.5, label_visibility="collapsed", key="rd_rate")
    st.button("Term", on_click=rd_term_calc, use_container_width=True)
    st.number_input("Term", min_value=0.0, step=1.0,  label_visibility="collapsed", key="rd_term")
    st.button("Maturity Value", on_click=rd_matu_calc, use_container_width=True)
    st.number_input("Maturity", min_value=0.0, step=1000.0, label_visibility="collapsed", key="rd_matu")
df = st.session_state.rd_df
if df.shape[0] > 0:
    st.write( df )
    st.write( "Total of Instalments : " + str( st.session_state.rdinstalment) )
    st.write( "Total Interest : " + str( st.session_state.rdinterest) )
    chartdata = df
    chartdata[ "Cumulative Interest" ] = chartdata[ "Interest" ].cumsum()
    chartdata[ "Cumulative Instalment" ] = chartdata[ "Instalment" ].cumsum()
    chartdata[ "Cumulative Interest" ] = chartdata[ "Cumulative Interest" ].round(2)
    chartdata[ "Cumulative Instalment" ] = chartdata[ "Cumulative Instalment" ].round(2)
    chartdata = chartdata[ [chartdata.columns[0], "Cumulative Interest", "Cumulative Instalment" ] ]
    chart_data_long = chartdata.melt(id_vars=chartdata.columns[0], var_name='Category', value_name='Value')
    chart = alt.Chart(chart_data_long).mark_area().encode(
        x=chartdata.columns[0]+':O',
        y='Value:Q',
        color='Category:N',
        tooltip=[chartdata.columns[0], 'Category', 'Value']
    )
    st.write(chart)
    base = alt.Chart(chartdata[ ["Cumulative Interest"] ], title="Cumulative Interest").encode(
        alt.Theta("Cumulative Interest:Q").stack(True),
        alt.Radius("Cumulative Interest").scale(type="sqrt", zero=True, rangeMin=20),
        color=alt.Color("Cumulative Interest:N").legend(None),
    )
    c1 = base.mark_arc(innerRadius=20, stroke="#fff")
    
    base1 = alt.Chart(chartdata[ ["Cumulative Instalment"] ], title="Cumulative Instalment").encode(
        alt.Theta("Cumulative Instalment:Q").stack(True),
        alt.Radius("Cumulative Instalment").scale(type="sqrt", zero=True, rangeMin=20),
        color=alt.Color("Cumulative Instalment:N").legend(None),
    )
    c2 = base1.mark_arc(innerRadius=20, stroke="#fff")
    [col11, col12] = st.columns([0.5, 0.5])
    with col11:
        st.write(c1)
    with col12:    
        st.write(c2)
    st.info("Done!")
    st.session_state.rd_df = pd.DataFrame( [] )
    st.session_state.rdinterest = 0.0
    st.session_state.rdinstalment = 0.0
