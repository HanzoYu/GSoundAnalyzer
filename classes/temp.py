    def analyzePeak1(self):
        """Analyze the peak in the selected region for signal 1
        
        Returns:
            None: Description
        """
        # Retrieving ROI data
        self.imin1 = int(self.min2*1000+0.5)
        self.imax1 = int(self.max2*1000+0.5)
        self.pw2.removeItem(self.plot5)
        self.pw2.removeItem(self.plot6)
        self.pw2.removeItem(self.plot9)
        if self.filterCoreSize1 <= 1:
            self.section1 = self.rawA1[self.imin1:self.imax1]
        else:
            #Medfilter defined in scipy
            #self.section1 = signal.medfilt(self.rawA1[self.imin1:self.imax1],
            #                               self.filterCoreSize1)
            #print (self.filterCoreSize1)
            self.section1 = self.rawA1[self.imin1:self.imax1]
            print (self.imin1, self.imax1, np.average(self.rawA1))
            self.movingAverage1()
        
        # Finding zero point
        self.section01 = self.section1[0:self.n01]
        self.avg1 = np.mean(self.section01)
        self.plot5 = self.pw2.plot(np.linspace(self.min2,
                                   self.min2+self.n01/self.f*1000,
                                   self.n01), np.ones(self.n01)*self.avg1,
                                   pen=pg.mkPen('c', width=2))

        # Finding maximum point
        self.ipeak1 = np.argmax(self.section1)
        self.Ap1 = np.amax(self.section1) - self.avg1

        # Finding half maximum points
        for i in range(0, self.ipeak1):
            if self.section1[i] >= self.Ap1*0.2+self.avg1: #0.1, 10% maximum, 0.5, half maximum
                break
        self.iFrontHM1 = i
        self.tp1 = self.iFrontHM1/1000.0+self.min2

        for i in range(self.ipeak1, self.imax1-self.imin1):
            if self.section1[i] <= self.Ap1*0.2+self.avg1: #0.1,0.2 or 0.5
                break
        self.iBackHM1 = i
        self.wp1 = (self.iBackHM1-self.iFrontHM1)/1000.0

        # Visualization
        self.plot6 = self.pw2.plot(np.linspace(self.tp1, self.tp1+self.wp1, self.iBackHM1-self.iFrontHM1), self.section1[self.iFrontHM1:self.iBackHM1], pen=pg.mkPen('b',width=2))
        self.plot9 = self.pw2.plot([self.tp1, self.ipeak1/1000.0+self.min2, self.tp1+self.wp1],[self.Ap1*0.2+self.avg1, self.Ap1+self.avg1, self.Ap1*0.2+self.avg1], pen=None, symbolBrush=('b'), symbolSize=7) #0.1 or 0.5

        # Updating results in the TextBoxs
        self.ApBox1.setText("%f" % self.Ap1)
        self.wpBox1.setText("%f" % self.wp1)
        self.tpBox1.setText("%f" % self.tp1)
