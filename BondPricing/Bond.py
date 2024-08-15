class Bond:
    def __init__(self, face_value, maturity, ytm, periods_per_year=1):
        self.face_value = face_value  # Face value (principal)
        self.maturity = maturity      # Time to maturity (in years)
        self.ytm = ytm                # Yield to maturity (annualized)
        self.periods_per_year = periods_per_year  # Payment frequency

    def price(self):
        raise NotImplementedError("Subclasses should implement this method.")

#fixed rate bond
class FixedRateBond(Bond):
    def __init__(self, face_value, maturity, ytm, coupon_rate, periods_per_year=1):
        super().__init__(face_value, maturity, ytm, periods_per_year)
        self.coupon_rate = coupon_rate  # Annual coupon rate

    def price(self):
        coupon_payment = (self.coupon_rate * self.face_value) / self.periods_per_year
        total_periods = self.maturity * self.periods_per_year
        
        #price by summing the present value of coupons and face value
        price = sum([coupon_payment / (1 + self.ytm/self.periods_per_year)**t for t in range(1, total_periods + 1)])
        price += self.face_value / (1 + self.ytm/self.periods_per_year)**total_periods
        
        return price
    
#zero coupon bond
class ZeroCouponBond(Bond):
    def __init__(self, face_value, maturity, ytm):
        super().__init__(face_value, maturity, ytm)
    
    def price(self):
        #price is the present value of the face value
        price = self.face_value / (1 + self.ytm)**self.maturity
        return price


#floating rate bond
class FloatingRateBond(Bond):
    def __init__(self, face_value, maturity, ytm, margin, reference_rates, periods_per_year=1):
        super().__init__(face_value, maturity, ytm, periods_per_year)
        self.margin = margin              # margin added to the reference rate
        self.reference_rates = reference_rates  # reference rates for each period
    
    def price(self):
        total_periods = len(self.reference_rates)
        price = 0
        
        #price by summing the present value of each coupon and face value
        for t in range(1, total_periods + 1):
            coupon_payment = (self.margin + self.reference_rates[t-1]) * self.face_value / self.periods_per_year
            discount_factor = (1 + self.ytm/self.periods_per_year)**t
            price += coupon_payment / discount_factor
        
        price += self.face_value / (1 + self.ytm/self.periods_per_year)**total_periods
        
        return price

class BondWithYieldCurve(Bond):
    def __init__(self, face_value, maturity, coupon_rate, yield_curve, periods_per_year=1):
        super().__init__(face_value, maturity, None, periods_per_year)
        self.coupon_rate = coupon_rate
        self.yield_curve = yield_curve
    
    def price(self):
        coupon_payment = (self.coupon_rate * self.face_value) / self.periods_per_year
        total_periods = len(self.yield_curve)
        
        price = sum([coupon_payment / (1 + self.yield_curve[t-1]/self.periods_per_year)**t for t in range(1, total_periods + 1)])
        price += self.face_value / (1 + self.yield_curve[-1]/self.periods_per_year)**total_periods
        
        return price