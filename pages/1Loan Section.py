import streamlit as st
import math
import pandas as pd
import altair as alt

# st.session_state.loan_prin = 0.0
# st.session_state.loan_rate = 0.0
# st.session_state.loan_term = 0.0
# st.session_state.loan_inst = 0.0
if 'loan_df' not in st.session_state:
    st.session_state.loan_df = pd.DataFrame( [] )
    st.session_state.interest = 0.0
    st.session_state.repayment = 0.0
comp_mapping = {
    "Monthly": 12,
    "Quarterly": 4,
    "Half Yearly": 2,
    "Yearly": 1
}

freq_mapping = {
    "Months": 12,
    "Quarters": 4,
    "Half Years": 2,
    "Years": 1
}


def showloanaccount():
    reportarr = []
    prin = st.session_state.loan_prin
    intrate = st.session_state.loan_rate / 100
    period = st.session_state.loan_term
    instal = st.session_state.loan_inst
    yearlycompoundings = comp_mapping.get(st.session_state.loan_comp)
    yearlyinstalments = freq_mapping.get(st.session_state.loan_freq)
    roundby = 2
    total1 = 0.0
    total2 = 0.0
    if yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings))
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments)
        head1 = st.session_state.loan_freq
        head1 = head1[:-1]
        counter = 1
        count1 = 1
        balance = prin
        totint = 0
        totinst = 0
        product = 0
        interest = 0
        while counter <= period:
            totinst = totinst + instal
            product = product + balance
            if math.fmod(counter,yearlyinstalments/yearlycompoundings) == 0:
                interest = round(product * m,roundby)
                totint = interest + totint
                product = 0.0
            if counter > (fulcomp / yearlycompoundings * yearlyinstalments):
                product = 0
                totinst = totinst - instal
                while count1 <= balacomp:
                    totinst = totinst + instal
                    product = product + balance
                    if counter == period:
                        interest = round(product * m,roundby)
                        totint = interest + totint
                        product = 0
                        reportarr.append(
                            {
                                head1: counter,
                                'Opening Balance': round(balance, roundby),
                                'Interest Charged': round(interest, roundby),
                                'Repayment': round(instal, roundby),
                                'Closing Balance': round(balance + interest - instal, roundby)
                            }    
                        )        
                    balance = balance + interest - instal
                    count1 = count1 + 1
                    counter = counter + 1
                    interest = 0
            if counter <= (fulcomp / yearlycompoundings * yearlyinstalments):
                reportarr.append(
                    {
                        head1: counter,
                        'Opening Balance': round(balance, roundby),
                        'Interest Charged': round(interest, roundby),
                        'Repayment': round(instal, roundby),
                        'Closing Balance': round(balance + interest - instal, roundby)
                    }    
                )        
                balance = balance + interest - instal
                counter = counter + 1
                interest = 0
        total1 = 0.0
        total2 = 0.0
        for i in reportarr:
            total1 = total1 + i["Interest Charged"]
            total2 = total2 + i["Repayment"]
    if yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings  
        n = (yearlycompoundings/yearlyinstalments)
        head1 = st.session_state.loan_freq
        head1 = head1[:-1]
        counter = 1
        count1 = 1
        instal1 = 0.0
        balance = prin
        totint = 0.0
        totinst = 0.0
        product = 0.0
        interest = 0.0
        comcount = 1
        inscount = 1
        while counter <= period * yearlycompoundings/yearlyinstalments:
            product = balance + product
            interest = round(product * m,roundby)
            totint = totint + interest
            product = 0.0
            if inscount == n:
                instal1 = instal
                totinst = totinst + instal1
                inscount = 0
            else:
                instal1 = 0
            reportarr.append(
                {
                    head1: counter,
                    'Opening Balance': round(balance, roundby),
                    'Interest Charged': round(interest, roundby),
                    'Repayment': round(instal1, roundby),
                    'Closing Balance': round(balance + interest - instal1, roundby)
                }    
            )        
            balance = balance + interest - instal1
            counter = counter + 1
            inscount = inscount + 1
            interest = 0
        total1 = 0.0
        total2 = 0.0
        for i in reportarr:
            total1 = total1 + i["Interest Charged"]
            total2 = total2 + i["Repayment"]
    st.session_state.loan_df = pd.DataFrame( reportarr )
    st.session_state.interest = round(total1, roundby)
    st.session_state.repayment = round(total2, roundby)
    


def loan_prin_calc():
    prin = 0.0
    intrate = st.session_state.loan_rate / 100
    period = st.session_state.loan_term
    instal = st.session_state.loan_inst
    yearlycompoundings = comp_mapping.get(st.session_state.loan_comp)
    yearlyinstalments = freq_mapping.get(st.session_state.loan_freq)
    m = 0.0
    fulcomp = 0.0
    balacomp = 0.0
    total1 = 0.0
    x = 0.0
    l = 0.0
    if (intrate == 0.0 or instal == 0.0 or period == 0.0):
        st.error("You have to enter Interest Rate, Instalment Amount and Term of the Loan to find out the Principal.")
    else:   
        if yearlyinstalments >= yearlycompoundings:
            m = intrate / yearlyinstalments
            fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
            balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
            total1 = 0.0
            x = yearlyinstalments / yearlycompoundings
            l = (x + (x * (x - 1) / 2 * m))/(1+(intrate / yearlycompoundings))
            if balacomp > 0:
               m1 = (balacomp+((balacomp*(balacomp-1)/2)*m))/(1+(m*balacomp))/(1+(intrate/yearlycompoundings))**fulcomp
               total1 = total1 + m1
            if fulcomp > 0:
               total1 = total1 + l
            for i in range(2, fulcomp + 1):
               l = l / (1+(intrate / yearlycompoundings))
               total1 = total1 + l
            prin = total1 * instal
        if yearlyinstalments < yearlycompoundings:
            m = intrate / yearlycompoundings
            n = (yearlycompoundings/yearlyinstalments)
            counter = 1
            l = 1
            total1 = 0.0
            while counter <= period:
               l = l/((1+m)**n)
               total1 = total1 + l
               counter = counter + 1
            prin = total1 * instal
    st.session_state.loan_prin = prin        
    showloanaccount()
    
def loan_term_calc():
    prin = st.session_state.loan_prin
    intrate = st.session_state.loan_rate / 100
    period = 0
    instal = st.session_state.loan_inst
    yearlycompoundings = comp_mapping.get(st.session_state.loan_comp)
    yearlyinstalments = freq_mapping.get(st.session_state.loan_freq)
    m = 0.0
    if (intrate == 0.0 or instal == 0.0 or prin == 0.0):
        st.error("You have to enter Interest Rate, Instalment Amount and Principal of the Loan to find out the Term of the Loan.")
    elif prin < instal:
        st.error("Principal amount must be greater than Instalment amount.")
    else:   
        if yearlyinstalments >= yearlycompoundings:
            m = intrate / yearlyinstalments
            if (prin * m) >= instal:
                st.error("The instalment amount is not enough even to cover the interest portion!")
            else:
                period = prin / instal
                crossed = False
                x = yearlyinstalments / yearlycompoundings
                while not crossed:
                    l = (x + (x * (x - 1) / 2 * m))/(1+(intrate / yearlycompoundings))
                    fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
                    balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
                    total1 = 0.0
                    if balacomp > 0:
                        m1 = (balacomp+((balacomp*(balacomp-1)/2)*m))/(1+(m*balacomp))/(1+(intrate/yearlycompoundings))**fulcomp
                        total1 = total1 + m1
                    if fulcomp > 0:
                        total1 = total1 + l
                    for i in range( 2,fulcomp + 1):  
                        l = l / (1+(intrate / yearlycompoundings))
                        total1 = total1 + l
                    if (total1*instal)- prin  > 0.0:
                        crossed = True
                    else:
                        period = period + 1
        if yearlyinstalments < yearlycompoundings:
            n = (yearlycompoundings/yearlyinstalments)
            m = intrate / yearlycompoundings
            interest = 0.0
            balance = prin
            for i in range(1, n+1):
                interest = interest + (balance * m)
                balance = prin + interest
            if instal <= interest:
                st.error("The instalment amount is not enough even to cover the interest portion!")
            else:    
                period = prin / instal
                crossed = False
            while not crossed:
                counter = 1
                l = 1
                total1 = 0.0
                while counter <= period:
                    l = l/((1+m)**n)
                    total1 = total1 + l
                    counter = counter + 1
                if (total1*instal)- prin  > 0.0:
                    crossed = True
                else:
                    period = period + 1
    st.session_state.loan_term = round(period)
    showloanaccount()
    

def loan_inst_calc():
    prin = st.session_state.loan_prin
    intrate = st.session_state.loan_rate / 100
    period = st.session_state.loan_term
    instal = 0.0
    yearlycompoundings = comp_mapping.get(st.session_state.loan_comp)
    yearlyinstalments = freq_mapping.get(st.session_state.loan_freq)
    m = 0.0
    if (intrate == 0.0 or prin == 0.0 or period == 0.0):
        st.error("You have to enter Principal Amount, Interest Rate, Instalment Amount to find out the Instalment Amount.")
    elif yearlyinstalments >= yearlycompoundings:
        m = intrate / yearlyinstalments
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings)) 
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        total1 = 0.0
        x = yearlyinstalments / yearlycompoundings
        l = (x + (x * (x - 1) / 2 * m))/(1+(intrate / yearlycompoundings))
        if balacomp > 0:
           m1 = (balacomp+((balacomp*(balacomp-1)/2)*m))/(1+(m*balacomp))/(1+(intrate/yearlycompoundings))**fulcomp
           total1 = total1 + m1
        if fulcomp > 0:
           total1 = total1 + l
        for i in range(2, fulcomp+1 ):
            l = l / (1+(intrate / yearlycompoundings))
            total1 = total1 + l
        instal = prin / total1
    elif yearlyinstalments < yearlycompoundings:
        m = intrate / yearlycompoundings
        n = (yearlycompoundings/yearlyinstalments)
        counter = 1
        l = 1
        total1 = 0.0
        while counter <= period:
            l = l/((1+m)**n)
            total1 = total1 + l
            counter = counter + 1
        instal = prin / total1
    st.session_state.loan_inst = instal    
    showloanaccount()
    

def loan_rate_calc():
    prin = st.session_state.loan_prin
    intrate = 0.0
    period = st.session_state.loan_term
    instal = st.session_state.loan_inst
    yearlycompoundings = comp_mapping.get(st.session_state.loan_comp)
    yearlyinstalments = freq_mapping.get(st.session_state.loan_freq)
    m = 0.0
    if (prin == 0.0 or instal == 0.0 or period == 0.0):
        st.error("You have to enter Principal Amount, Instalment Amount and Term of the Loan to find out the Interest Rate.")
    elif period * instal < prin:
        st.error("The total instalments payable can not be below the principal value!!!")
    elif yearlyinstalments >= yearlycompoundings:
        fulcomp = int(period / (yearlyinstalments / yearlycompoundings))
        balacomp = period - (fulcomp / yearlycompoundings * yearlyinstalments) 
        intrate = 0.00001
        crossed = False
        centpercentwarn = False
        while not crossed:
            total1 = 0.0
            m = intrate / yearlyinstalments
            x = yearlyinstalments / yearlycompoundings
            l = (x + (x * (x - 1) / 2 * m))/(1+(intrate / yearlycompoundings))
            if balacomp > 0:
                m1 = (balacomp+((balacomp*(balacomp-1)/2)*m))/(1+(m*balacomp))/(1+(intrate/yearlycompoundings))**fulcomp
                total1 = total1 + m1
            if fulcomp > 0:
                total1 = total1 + l
            for i in range(2, fulcomp + 1 ):
                l = l / (1+(intrate / yearlycompoundings))
                total1 = total1 + l
            if (total1*instal)- prin  < 0.0:
                crossed = True
                if centpercentwarn:
                    st.warning("Caution. Interest Rate goes beyond 100%! "+str(intrate*100))
            else:
                if ((total1*instal)-prin)/prin > 0.01:
                    intrate = intrate + 0.0001
                else:
                    intrate = intrate + 0.00001
                if intrate > 1 and not centpercentwarn:
                    st.warning("Caution. Interest Rate goes beyond 100%! ")
                    centpercentwarn = True
    elif yearlyinstalments < yearlycompoundings:
        n = (yearlycompoundings/yearlyinstalments)
        intrate = 0.00001
        crossed = False
        centpercentwarn = False
        while not crossed:
            counter = 1
            l = 1
            m = intrate / yearlycompoundings
            total1 = 0.0
            while counter <= period:
                l = l/((1+m)**n)
                total1 = total1 + l
                counter = counter + 1
            if (total1*instal)- prin  < 0.0:
                crossed = True
                if centpercentwarn:
                    st.warning("Caution. Interest Rate goes beyond 100%! "+str(intrate*100))
            else:
                if ((total1*instal)-prin)/prin > 0.01:
                    intrate = intrate + 0.0001
                else:
                    intrate = intrate + 0.00001
                if intrate > 1 and not centpercentwarn:
                    st.warning("Caution. Interest Rate goes beyond 100%! ")
                    centpercentwarn = True
    st.session_state.loan_rate = intrate * 100
    showloanaccount()

    
[image,title] = st.columns([0.5,0.5])
with image:
    st.image("./pages/LoanSection.jpg")
with title:   
    st.write("# :red[Loan Section]")
[col1, col2] = st.columns([0.5, 0.5])
with col1:
    st.button("Interest Compounding", disabled=True, use_container_width=True)
    st.selectbox("Compounding",("Monthly", "Quarterly","Half Yearly","Yearly"), label_visibility="collapsed", key="loan_comp")
    st.button("Principal", on_click=loan_prin_calc, use_container_width=True)
    st.number_input("Principal", min_value=0.0, label_visibility="collapsed", key="loan_prin")
    st.button("Interest Rate (% p.a.)", on_click=loan_rate_calc, use_container_width=True)
    st.number_input("Interest Rate", min_value=0.0, label_visibility="collapsed", key="loan_rate")
    st.button("Term", on_click=loan_term_calc, use_container_width=True)
    st.number_input("Term", min_value=0.0,  label_visibility="collapsed", key="loan_term")
    st.button("Instalment", on_click=loan_inst_calc, use_container_width=True)
    st.number_input("Instalment", min_value=0.0, label_visibility="collapsed", key="loan_inst")
    st.button("Instalment Frequency", disabled=True, use_container_width=True)
    st.selectbox("Frequency",("Months", "Quarters","Half Years","Years"), label_visibility="collapsed", key="loan_freq")

df = st.session_state.loan_df
if df.shape[0] > 0:
    st.write( df )
    st.write( "Total Interest : " + str( st.session_state.interest) )
    st.write( "Total Repayment : " + str( st.session_state.repayment) )
    chartdata = df
    chartdata[ "Principal" ] = chartdata[ "Repayment" ] - chartdata[ "Interest Charged" ]
    chartdata = chartdata[ [chartdata.columns[0], "Interest Charged", "Principal" ] ]
    chart_data_long = chartdata.melt(id_vars=chartdata.columns[0], var_name='Category', value_name='Value')
    chart = alt.Chart(chart_data_long).mark_bar().encode(
        x=chartdata.columns[0]+':O',
        y='Value:Q',
        color='Category:N',
        tooltip=[chartdata.columns[0], 'Category', 'Value']
    )
    st.write(chart)
    base = alt.Chart(df[ ["Closing Balance"] ], title="Closing Balance").encode(
        alt.Theta("Closing Balance:Q").stack(True),
        alt.Radius("Closing Balance").scale(type="sqrt", zero=True, rangeMin=20),
        color=alt.Color("Closing Balance:N").legend(None),
    )
    c1 = base.mark_arc(innerRadius=20, stroke="#fff")
    st.write(c1)
    st.session_state.loan_df = pd.DataFrame( [] )
    st.session_state.interest = 0.0
    st.session_state.repayment = 0.0
