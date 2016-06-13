
import math

def HitsMatch( Hit1, Hit2 ):
	
	if ( Hit1.BX() == Hit2.BX() and Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector() ):
		if ( Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire() ):
			return True
		else:
			return False
	else:
		return False

def CalcPhiGlobDeg( phi_loc_int, sector ):
	
	phi_loc_deg = ( phi_loc_int / 60.0 ) - 22
	phi_glob_deg = phi_loc_deg + 60 * (sector - 1) + 15

	if (phi_glob_deg <   0): phi_glob_deg = phi_glob_deg + 360
	if (phi_glob_deg > 360): phi_glob_deg = phi_glob_deg - 360
	return phi_glob_deg

def HitPhiInChamber( Hit ):

	## phi_glob_deg = CalcPhiGlobDeg( Hit.Phi_loc_int(), Hit.Sector() )
	phi_glob_deg = Hit.Phi_glob_deg()
	if (phi_glob_deg <   0): phi_glob_deg = phi_glob_deg + 360
	if (phi_glob_deg > 360): phi_glob_deg = phi_glob_deg - 360

	# phi_loc_deg_corr = (Hit.Phi_loc_int() / (0.625 * 60)) * 0.97975745
	# phi_GMT = math.floor(phi_loc_deg_corr - 35)
	# phi_loc_deg = (phi_GMT * 0.625) + 0.3125
	# phi_glob_deg = phi_loc_deg + 60 * (Hit.Sector() - 1) + 15
	# if (phi_glob_deg > 180): phi_glob_deg = 360 - phi_glob_deg

	if ( Hit.Station() != 1 and Hit.Ring() == 1 ):
		chamber_center = 20.0 * (Hit.Chamber() - 1) + 5.0
		chamber_half_width = 10 + 5 ## 1.5
	else:
		chamber_center = 10.0 * (Hit.Chamber() - 1)
		chamber_half_width = 5 + 2.5 ## 0.75
	if (chamber_center <   0): chamber_center = chamber_center + 360
	if (chamber_center > 360): chamber_center = chamber_center - 360

	pi = 3.14159265358979323846
	return math.asin( math.sin( (phi_glob_deg - chamber_center)*(pi/180) ) ) * (180/pi)
		
	# if phi_glob_deg > 90 or phi_glob_deg < 270:
		# if abs(phi_glob_deg - chamber_center) > chamber_half_width:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d has phi %.2f' % ( Hit.Station(), Hit.Sector(), Hit.Ring(),
		# 										   Hit.Chamber(), phi_glob_deg )
		# 	print 'Epected chamber range is %.2f to %.2f' % ( chamber_center - chamber_half_width, 
		# 							  chamber_center + chamber_half_width )
		# else:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d OK!' % ( Hit.Station(), Hit.Sector(), Hit.Ring(), Hit.Chamber() )
		# return phi_glob_deg - chamber_center

	# else:
		# if phi_glob_deg > 180:
			# phi_glob_deg = phi_glob_deg - 360
		# if chamber_center > 180:
			# chamber_center = chamber_center - 360
		# if abs(phi_glob_deg - chamber_center) > chamber_half_width:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d has phi %.2f' % ( Hit.Station(), Hit.Sector(), Hit.Ring(),
		# 										   Hit.Chamber(), phi_glob_deg )
		# 	print 'Epected chamber range is %.2f to %.2f' % ( chamber_center - chamber_half_width, 
		# 							  chamber_center + chamber_half_width )
		# else:
		# 	print 'Hit in station %d, sector %d, ring %d, chamber %d OK!' % ( Hit.Station(), Hit.Sector(), Hit.Ring(), Hit.Chamber() )
		# return phi_glob_deg - chamber_center
	
def TracksMatch( Trk1, Trk2 ):

	# ## if ( Trk1.First_BX() == Trk2.First_BX() and abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 2 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 5 ):
	# if ( abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 5 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 5 ):
	# 	return True
	# else:
	# 	return False

	phi_loc_deg_corr = (Trk1.Phi_loc_int() / (0.625 * 60)) * 0.979755
	phi_GMT = math.floor(phi_loc_deg_corr - 35)

	if (Trk1.Phi_GMT() != phi_GMT):
		print 'Trk1 phi_GMT (calc) = %d (%d) from phi_loc %d' % (Trk1.Phi_GMT(), phi_GMT, Trk1.Phi_loc_int())
	
	if ( Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.Sector() == Trk2.Sector() and Trk1.Phi_GMT() != Trk2.Phi_GMT() ):
		print 'Trk1 phi_loc (GMT) = %d (%d), Trk2 phi_loc (GMT) = %d (%d)' % ( Trk1.Phi_loc_int() , Trk1.Phi_GMT(), Trk2.Phi_loc_int() , Trk2.Phi_GMT() )
	
	## Exact match requirement
	if Trk1.Eta_GMT() == Trk2.Eta_GMT() and Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.BX() == Trk2.BX() and Trk1.Mode() == Trk2.Mode():
		return True
	else:
		return False

	if ( abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 6 ):
		if ( abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 6 ):
			return True
		# elif ( Trk1.Sector() == Trk2.Sector() + 1 and abs(Trk1.Phi_GMT() + 95 - Trk2.Phi_GMT()) < 8 ):
		# 	return True
		# elif ( Trk1.Sector() == 1 and Trk2.Sector() == 6 and abs(Trk1.Phi_GMT() + 95 - Trk2.Phi_GMT()) < 8 ):
		# 	return True
		else:
			return False
	else:
		return False
	

def PtLutAddrMatch( Trk1, Trk2 ):

	# ## Eta address is still screwed up - AWB 29.04.16
	# if ( Trk1.Pt_LUT_addr() == Trk2.Pt_LUT_addr() ): return True
	# else: return False

	if ( Trk1.DPhi_12() == Trk2.DPhi_12() and Trk1.DPhi_13() == Trk2.DPhi_13() and Trk1.DPhi_14() == Trk2.DPhi_14() and
	     Trk1.DPhi_23() == Trk2.DPhi_23() and Trk1.DPhi_24() == Trk2.DPhi_24() and Trk1.DPhi_34() == Trk2.DPhi_34() and
	     Trk1.DTheta_12() == Trk2.DTheta_12() and Trk1.DTheta_13() == Trk2.DTheta_13() and Trk1.DTheta_14() == Trk2.DTheta_14() and
	     Trk1.DTheta_23() == Trk2.DTheta_23() and Trk1.DTheta_24() == Trk2.DTheta_24() and Trk1.DTheta_34() == Trk2.DTheta_34() and
	     Trk1.CLCT_1() == Trk2.CLCT_1() and Trk1.CLCT_2() == Trk2.CLCT_2() and Trk1.CLCT_3() == Trk2.CLCT_3() and Trk1.CLCT_4() == Trk2.CLCT_4() and
	     True ):
	     # Trk1.FR_1() == Trk2.FR_1() and Trk1.FR_2() == Trk2.FR_2() and Trk1.FR_3() == Trk2.FR_3() and Trk1.FR_4() == Trk2.FR_4() ):
		return True
	else: return False


def PrintEMTFHit( Hit ):
	print 'BX = %d, station = %d, sector = %d, subsector = %d, ring = %d, ' % ( Hit.BX(), Hit.Station(), Hit.Sector(), Hit.Subsector(), Hit.Ring() ), \
	    'CSC ID = %d, chamber = %d, strip = %d, wire = %d, neighbor = %d' % ( Hit.CSC_ID(), Hit.Chamber(), Hit.Strip(), Hit.Wire(), Hit.Neighbor() )

def PrintEMTFHitExtra( Hit ):
	PrintEMTFHit( Hit )
	## print 'phi_loc_int = %d, theta_int = %d, phi_glob_deg = %.1f, eta = %.3f' % ( Hit.Phi_loc_int(), Hit.Theta_int(), Hit.Phi_glob_deg(), Hit.Eta() )
	print 'phi_loc_int = %d, theta_int = %d, phi_glob_deg = %.1f, eta = %.3f' % ( Hit.Phi_loc_int(), Hit.Theta_int(), CalcPhiGlobDeg( Hit.Phi_loc_int(), Hit.Sector() ), Hit.Eta() )

def PrintEMTFTrack( Trk ):
	print 'BX = %d, sector = %d, mode = %d, phi_loc_int = %d, phi_GMT = %d, ' % ( Trk.BX(), Trk.Sector(), Trk.Mode(), Trk.Phi_loc_int(), Trk.Phi_GMT() ), \
	    'eta_GMT = %d, pT_GMT = %d, phi_glob_deg = %.1f, eta = %.3f, pT = %.1f, ' % ( Trk.Eta_GMT(), Trk.Pt_GMT(), Trk.Phi_glob_deg(), Trk.Eta(), Trk.Pt() )
	    # 'has some (all) neighbor hits = %d (%d)' % ( Trk.Has_neighbor(), Trk.All_neighbor() ) 
	
def PrintSimulatorHitHeader():
	print 'EMULATOR HITS FOR SIMULATOR: time_bin, endcap, sector, subsector, station, valid, quality, CLCT pattern, wiregroup, cscid, bend, halfstrip'

def PrintSimulatorHit( Hit ):
	if Hit.Endcap() == 1:
		tmp_endcap = 1
	else:
		tmp_endcap = 2
	if Hit.Subsector() < 0:
		tmp_sub = 0
	else:
		tmp_sub = Hit.Subsector()
	if Hit.Ring() == 4:
		tmp_id = Hit.CSC_ID() + 9
	else:
		tmp_id = Hit.CSC_ID()
	if Hit.Bend() < 0:
		tmp_bend = 0
	else:
		tmp_bend = Hit.Bend()
	print '%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d' % ( Hit.BX() + 6, tmp_endcap, Hit.Sector(), tmp_sub, Hit.Station(), Hit.Valid(),
								 Hit.Quality(), Hit.Pattern(), Hit.Wire(), tmp_id, tmp_bend, Hit.Strip() )

def PrintPtLUT( Trk ):

	if (Trk.DPhi_12() != -999): print('dPhi_12 = %d,' % Trk.DPhi_12()), 
	if (Trk.DPhi_13() != -999): print('dPhi_13 = %d,' % Trk.DPhi_13()), 
	if (Trk.DPhi_14() != -999): print('dPhi_14 = %d,' % Trk.DPhi_14()), 
	if (Trk.DPhi_23() != -999): print('dPhi_23 = %d,' % Trk.DPhi_23()), 
	if (Trk.DPhi_24() != -999): print('dPhi_24 = %d,' % Trk.DPhi_24()), 
	if (Trk.DPhi_34() != -999): print('dPhi_34 = %d,' % Trk.DPhi_34()),
	if (Trk.DTheta_12() != -999): print('dTheta_12 = %d,' % Trk.DTheta_12()), 
	if (Trk.DTheta_13() != -999): print('dTheta_13 = %d,' % Trk.DTheta_13()), 
	if (Trk.DTheta_14() != -999): print('dTheta_14 = %d,' % Trk.DTheta_14()), 
	if (Trk.DTheta_23() != -999): print('dTheta_23 = %d,' % Trk.DTheta_23()), 
	if (Trk.DTheta_24() != -999): print('dTheta_24 = %d,' % Trk.DTheta_24()), 
	if (Trk.DTheta_34() != -999): print('dTheta_34 = %d,' % Trk.DTheta_34()),
	if (Trk.CLCT_1() != -999): print('clct_1 = %d,' % Trk.CLCT_1()),
	if (Trk.CLCT_2() != -999): print('clct_2 = %d,' % Trk.CLCT_2()),
	if (Trk.CLCT_3() != -999): print('clct_3 = %d,' % Trk.CLCT_3()),
	if (Trk.CLCT_4() != -999): print('clct_4 = %d,' % Trk.CLCT_4()),
	if (Trk.FR_1() != -999): print('fr_1 = %d,' % Trk.FR_1()),
	if (Trk.FR_2() != -999): print('fr_2 = %d,' % Trk.FR_2()),
	if (Trk.FR_3() != -999): print('fr_3 = %d,' % Trk.FR_3()),
	if (Trk.FR_4() != -999): print('fr_4 = %d,' % Trk.FR_4()),
	print ''
