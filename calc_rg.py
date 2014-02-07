from numpy import *

scattering_coefficients = empty([4, 21, 19, 100])

for l in range(scattering_coefficients.shape[0]):
	for sg in range(scattering_coefficients.shape[1]):
		filename = 'lookup_tables/lambda=' + str(l+1) + '_sigma=' + str(sg+1) + '.csv'
		scattering_coefficients[l,sg,:,:] = genfromtxt(filename, delimiter=',')

theoretical_ratios = empty([
	scattering_coefficients.shape[0]-1,
	scattering_coefficients.shape[1],
	scattering_coefficients.shape[2],
	scattering_coefficients.shape[3]
	])

for i in range(theoretical_ratios.shape[0]):
	for sg in range(theoretical_ratios.shape[1]):
		for m in range(theoretical_ratios.shape[2]):
			for rg in range(theoretical_ratios.shape[3]):
				if i == 0:
					l = i
				else:
					l = i + 1
				theoretical_ratios[i,sg,m,rg] = scattering_coefficients[l,sg,m,rg]/scattering_coefficients[1,sg,m,rg]


def calc_rg(absorbtions):

	experimental_ratios = array([
		absorbtions[0]/absorbtions[1], 
		absorbtions[2]/absorbtions[1], 
		absorbtions[3]/absorbtions[1]
		])

	radii = linspace(.01,1,100)
	refractive_indeces = linspace(1.33,1.51,19)
	sigmas = linspace(1.3,1.42,13)

	r_lower = 0
	r_upper = len(radii) - 1
	m_lower = 0
	m_upper = len(refractive_indeces) - 1
	s_lower = 0
	s_upper = len(sigmas) - 1
	

	error = 1

	while r_lower < r_upper:
		r_mid = (r_upper+r_lower)/2
		m_mid = (m_upper+m_lower)/2
		s_mid = (s_upper+s_lower)/2

		test_points = array([
			[(r_mid+r_upper)/2,(m_mid+m_upper)/2,(s_mid+s_upper)/2],
			[(r_mid+r_upper)/2,(m_mid+m_upper)/2,(s_mid+s_lower)/2],
			[(r_mid+r_upper)/2,(m_mid+m_lower)/2,(s_mid+s_upper)/2],
			[(r_mid+r_upper)/2,(m_mid+m_lower)/2,(s_mid+s_lower)/2],
			[(r_mid+r_lower)/2,(m_mid+m_upper)/2,(s_mid+s_upper)/2],
			[(r_mid+r_lower)/2,(m_mid+m_upper)/2,(s_mid+s_lower)/2],
			[(r_mid+r_lower)/2,(m_mid+m_lower)/2,(s_mid+s_upper)/2],
			[(r_mid+r_lower)/2,(m_mid+m_lower)/2,(s_mid+s_lower)/2]
			])

		
		best_fit = -1

		for i in range(len(test_points)):
			test_error = 0
			for j in range(len(experimental_ratios)):
				test_error += (experimental_ratios[j] - theoretical_ratios[j,test_points[i,2],test_points[i,1],test_points[i,0]])**2
			if test_error < error:
				error = test_error
				best_fit = i

		if best_fit == 0:
			r_lower = r_mid
			m_lower = m_mid
			s_lower = s_mid
		elif best_fit == 1:
			r_lower = r_mid
			m_lower = m_mid
			s_upper = s_mid
		elif best_fit == 2:
			r_lower = r_mid
			m_upper = m_mid
			s_lower = s_mid
		elif best_fit == 3:
			r_lower = r_mid
			m_upper = m_mid
			s_upper = s_mid
		elif best_fit == 4:
			r_upper = r_mid
			m_lower = m_mid
			s_lower = s_mid
		elif best_fit == 5:
			r_upper = r_mid
			m_lower = m_mid
			s_upper = s_mid
		elif best_fit == 6:
			r_upper = r_mid
			m_upper = m_mid
			s_lower = s_mid
		elif best_fit == 7:
			r_upper = r_mid
			m_upper = m_mid
			s_upper = s_mid
		else:
			r_upper = test_points[0,0]
			r_lower = test_points[7,0]
			m_upper = test_points[0,1]
			m_lower = test_points[7,1]
			s_upper = test_points[0,2]
			s_lower = test_points[7,2]
	return [
		radii[r_lower], 
		refractive_indeces[m_lower], 
		sigmas[s_lower], 
		dot(squeeze(scattering_coefficients[:,s_lower,m_lower,r_lower]),.0001**2),
		error]
