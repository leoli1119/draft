# ----------------------------------------------
# lihuan 20180305
# ANSYS Electronics Desktop
# ----------------------------------------------

#################################### ------- input ------- ####################

import os
datainputfile = os.getenv("TEMP") + "\DiffViaGenDataInputFile.py"

with open(datainputfile,"r") as datafile:
	for exeline in datafile.readlines():
		exec(exeline.strip())

# angle value add unit "deg"

p_RefViatoYaxis_Angle = p_RefViatoYaxis_Angle + "deg"
n_RefViatoYaxis_Angle = n_RefViatoYaxis_Angle + "deg"

################################### ------- input ------- ######################

####   ----- def function -----
def addmaterial(obj, Tname, TdkORpermeability, TdfORcond) :
	if Tname[0:3].lower() != "cop" :
		obj.AddMaterial(
			[
				"NAME:" + Tname ,
				"CoordinateSystemType:=", "Cartesian",
				"BulkOrSurfaceType:="	, 1,
				[
					"NAME:PhysicsTypes",
					"set:="			, ["Electromagnetic","Thermal","Structural"]
				],
				"permittivity:="	, TdkORpermeability ,
				"dielectric_loss_tangent:=", TdfORcond ,
				"thermal_conductivity:=", "0.294",
				"mass_density:="	, "1900",
				"specific_heat:="	, "1150",
				"youngs_modulus:="	, "11000000000",
				"poissons_ratio:="	, "0.28",
				"thermal_expansion_coeffcient:=", "1.5e-005"
			])
	else :
		obj.AddMaterial(
			[
				"NAME:" + Tname ,
				"CoordinateSystemType:=", "Cartesian",
				"BulkOrSurfaceType:="	, 1,
				[
					"NAME:PhysicsTypes",
					"set:="			, ["Electromagnetic","Thermal","Structural"]
				],
				"permeability:="	, TdkORpermeability ,
				"conductivity:="	, TdfORcond ,
				"thermal_conductivity:=", "400",
				"mass_density:="	, "8933",
				"specific_heat:="	, "385",
				"youngs_modulus:="	, "120000000000",
				"poissons_ratio:="	, "0.38",
				"thermal_expansion_coeffcient:=", "1.77e-005"
			])
	return

def creatbox(obj, xP, yP, zP, xL, yL, zL, Tname, Tcolor, Num_trans, Tmate) :
	obj.CreateBox(
		[
			"NAME:BoxParameters",
			"XPosition:="		, xP ,
			"YPosition:="		, yP ,
			"ZPosition:="		, zP ,
			"XSize:="		, xL ,
			"YSize:="		, yL ,
			"ZSize:="		, zL 
		], 
		[
			"NAME:Attributes",
			"Name:="		, Tname ,
			"Flags:="		, "",
			"Color:="		, Tcolor ,
			"Transparency:="	, Num_trans ,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"" + Tmate + "\"" ,
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, Tmate != "Copper_5d8E7",   # False for metal, True for PP
			"IsMaterialEditable:="	, True
		])
	return

def createcylinder(obj, xP, yP, zP, Rradius, Lheight, Tname, Tcolor, Num_trans, Tmate) :
	obj.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, xP ,
			"YCenter:="		, yP ,
			"ZCenter:="		, zP ,
			"Radius:="		, Rradius ,
			"Height:="		, Lheight ,
			"WhichAxis:="		, "Z",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, Tname ,
			"Flags:="		, "",
			"Color:="		,  Tcolor ,
			"Transparency:="	, Num_trans ,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	,  "\"" + Tmate + "\"" ,
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, Tmate != "Copper_5d8E7",   # False for metal, True for PP
			"IsMaterialEditable:="	, True
		])	
	return		

def subtract(obj, Tblankpart, Ltoolpart, Bool_KeepOriginal) :
	Ltoolpart_ = Ltoolpart[0]
	if len( Ltoolpart ) > 1 :
		for i,v in enumerate( Ltoolpart ) :
			if i > 0 :
				Ltoolpart_ += ("," + v)
	obj.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, Tblankpart ,
			"Tool Parts:="		, Ltoolpart_
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, Bool_KeepOriginal
		])
	return

def unite( obj, Ltoolpart, Bool_KeepOriginal ) :
	Ltoolpart_ = Ltoolpart[0]
	if len( Ltoolpart ) > 1 :
		for i,v in enumerate( Ltoolpart ) :
			if i > 0 :
				Ltoolpart_ += ("," + v)
	obj.Unite(
		[
			"NAME:Selections",
			"Selections:="		, Ltoolpart_ 
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, Bool_KeepOriginal
		])	
	return

# get voidstruct, ellipsoid void on plane
def ellipsoid_voidstruct( obj , Space_via2via_t , D_antipad_t , Z_startvalue_t, thick_t , voidstruct_name_t ) :
	creatbox(obj, Space_via2via_t + "/2*(-1)", D_antipad_t + "/2*(-1) ", Z_startvalue_t,\
			Space_via2via_t, D_antipad_t, thick_t,\
			voidstruct_name_t, "(143 175 143)" , 0, "vacuum")
	createcylinder(obj, Space_via2via_t + "/2", "0mil", Z_startvalue_t,\
			D_antipad_t + "/2", thick_t,\
			voidstruct_name_t + "_Pvoid_ellipsoid", "(143 175 143)", 0, "vacuum")		
	createcylinder(obj, Space_via2via_t + "/2*(-1)", "0mil", Z_startvalue_t,\
			D_antipad_t + "/2", thick_t,\
			voidstruct_name_t + "_Nvoid_ellipsoid", "(143 175 143)", 0, "vacuum")		
	Ltoolpart_t = [voidstruct_name_t, voidstruct_name_t + "_Pvoid_ellipsoid", voidstruct_name_t + "_Nvoid_ellipsoid"]
	unite( obj, Ltoolpart_t, False )
	return 	

# get voidstruct, rectangle void on plane 
def rectangle_voidstruct( obj , Space_via2via_t , RectAnti_toLongside_t, RectAnti_toshortside_t, Z_startvalue_t, thick_t , voidstruct_name_t ) :
	creatbox(obj, Space_via2via_t + "/2*(-1)" + "+" + RectAnti_toshortside_t + "*(-1)" , RectAnti_toLongside_t + "*(-1) ", Z_startvalue_t,\
			Space_via2via_t + "+" + RectAnti_toshortside_t + "*2 ", RectAnti_toLongside_t + "*2 ", thick_t,\
			voidstruct_name_t, "(143 175 143)" , 0, "vacuum")
	return 

# get voidstruct, circle void on plane
def circle_voidstruct( obj , Space_via2via_t , D_cirantipad_t , Z_startvalue_t, thick_t , voidstruct_name_t ) :
	createcylinder(obj, Space_via2via_t + "/2", "0mil", Z_startvalue_t,\
			D_cirantipad_t + "/2", thick_t,\
			voidstruct_name_t + "_Pvoid_cir", "(143 175 143)", 0, "vacuum")		
	createcylinder(obj, Space_via2via_t + "/2*(-1)", "0mil", Z_startvalue_t,\
			D_cirantipad_t + "/2", thick_t,\
			voidstruct_name_t + "_Nvoid_cir", "(143 175 143)", 0, "vacuum")		
	return 	
	
	
# add Rectangle sheet
def addrect( obj, LCrossSectionXYZ_t, LWandH_t, Tname, Tcolor, Num_trans, Tmate) :
	# rectangle cross section
	obj.CreateRectangle(
		[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, LCrossSectionXYZ_t[0] ,
		"YStart:="		, LCrossSectionXYZ_t[1] ,
		"ZStart:="		, LCrossSectionXYZ_t[2] ,
		"Width:="		, LWandH_t[0] ,
		"Height:="		, LWandH_t[1] ,
		"WhichAxis:="		, "Y"
		], 
		[
			"NAME:Attributes",
			"Name:="		, Tname,
			"Flags:="		, "",
			"Color:="		, Tcolor,
			"Transparency:="	, Num_trans,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	,  "\"" + Tmate + "\"" ,
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		,  Tmate != "Copper_5d8E7",   # False for metal, True for PP
			"IsMaterialEditable:="	, True
		])		

# add rectangle cross section signal trace
# LCrossSectionXYZ_t -> [x,y,z] ; LWandH_t -> [w,h] ; Lpath_3pXYZ -> [(x0,y0,z0),(x1,y1,z1),(x2,y2,z2)]
def addrecttrace( obj, LCrossSectionXYZ_t, LWandH_t, Lpath_3pXYZ, Tname, Tcolor, Num_trans, Tmate) :
	# rectangle cross section
	addrect( obj, LCrossSectionXYZ_t, LWandH_t, Tname, Tcolor, Num_trans, Tmate)	
	obj.CreatePolyline(
		[
			"NAME:PolylineParameters",
			"IsPolylineCovered:="	, True,
			"IsPolylineClosed:="	, False,
			[
				"NAME:PolylinePoints",
				[
					"NAME:PLPoint",
					"X:="			, Lpath_3pXYZ[0][0],
					"Y:="			, Lpath_3pXYZ[0][1],
					"Z:="			, Lpath_3pXYZ[0][2]
				],
				[
					"NAME:PLPoint",
					"X:="			, Lpath_3pXYZ[1][0],
					"Y:="			, Lpath_3pXYZ[1][1],
					"Z:="			, Lpath_3pXYZ[1][2]
				],
				[
					"NAME:PLPoint",
					"X:="			, Lpath_3pXYZ[2][0],
					"Y:="			, Lpath_3pXYZ[2][1],
					"Z:="			, Lpath_3pXYZ[2][2]
				]
			],
			[
				"NAME:PolylineSegments",
				[
					"NAME:PLSegment",
					"SegmentType:="		, "Line",
					"StartIndex:="		, 0,
					"NoOfPoints:="		, 2
				],
				[
					"NAME:PLSegment",
					"SegmentType:="		, "Line",
					"StartIndex:="		, 1,
					"NoOfPoints:="		, 2
				]
			],
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0mil",
				"XSectionTopWidth:="	, "0mil",
				"XSectionHeight:="	, "0mil",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, Tname + "_TraceSweepPath",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"IsMaterialEditable:="	, True
		])	
	obj.SweepAlongPath(
		[
			"NAME:Selections",
			"Selections:="		, Tname + "," + Tname + "_TraceSweepPath",
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:PathSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"TwistAngle:="		, "0deg"
		])	
	return

# add local variable , obj -> oDesign
def addlocalvariable( obj, Tvariablename, Tdefaultvalue, Tdescription) :
	obj.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:LocalVariableTab",
				[
					"NAME:PropServers", 
					"LocalVariables"
				],
				[
					"NAME:NewProps",
					[
						"NAME:" + Tvariablename ,
						"PropType:="		, "VariableProp",
						"UserDef:="		, True,
						"Value:="		, Tdefaultvalue
					]
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:" + Tvariablename ,
						"Description:="		, Tdescription
					]
				]
			]
		])
	
	
####   ----- def function -----

# begin here # *****************************************************************
##### ------++--- project --+++---
SProjectName = "HFSSDesign_via"

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", SProjectName, "DrivenTerminal", "")

#_#   design editor
oDesign = oProject.SetActiveDesign( SProjectName )
oEditor = oDesign.SetActiveEditor("3D Modeler")

# design setting
oDesign.SetDesignSettings(
	[
		"NAME:Design Settings Data",
		"Use Advanced DC Extrapolation:=", False,
		"Use Power S:="		, False,
		"Export After Simulation:=", False,
		"Allow Material Override:=", True,
		"Calculate Lossy Dielectrics:=", True,
		"Perform Minimal validation:=", False,
		"EnabledObjects:="	, [],
		"Port Validation Settings:=", "Standard"
	], 
	[
		"NAME:Model Validation Settings",
		"EntityCheckLevel:="	, "Strict",
		"IgnoreUnclassifiedObjects:=", False,
		"SkipIntersectionChecks:=", False
	])

# add local variable
local_variable_list = [ \
("t_Lsize_x", t_Lsize_x, "PCB block X size"), \
("t_Lsize_y", t_Lsize_y, "PCB block Y size"), \
("t_D_pad", t_D_pad, "VIA pad diameter"), \
("t_D_drill", t_D_drill, "VIA drill diameter"), \
("t_Space_via2via", t_Space_via2via, "distance of signal via center to signal via center"), \
# t_D_cirantipad
("p_RefViatoSigVia_Distance", p_RefViatoSigVia_Distance, "distance of GND_p via center to signal via center"), \
("p_RefViatoYaxis_Angle", p_RefViatoYaxis_Angle, "Angle(0-180 degree) of GND_p via and Y axis"), \
("n_RefViatoSigVia_Distance", n_RefViatoSigVia_Distance, "distance of GND_n via center to signal via center"), \
("n_RefViatoYaxis_Angle", n_RefViatoYaxis_Angle, "Angle(0-180 degree) of GND_n via and Y axis"), \
#
("t_backdrill_stub", t_backdrill_stub, "after backdrill, the stub length to the backdrill_bottom layer, normal 10mil"), \
("t_D_backdrill", t_D_backdrill, "VIA backdrill diameter"), \
("t_Tplating", t_Tplating, "VIA plating thick"), \
("t_W_trace", t_W_trace, "width of diff signal trace"), \
("t_S_trace", t_S_trace, "space of diff signal trace") \
]

if t_ShapeAntipad == "1" :  #rect anti
	local_variable_list.append( ("t_RectAnti_toLongside", t_RectAnti_toLongside, "rectangle anti-pad, space of signal via center to long side") )
	local_variable_list.append( ("t_RectAnti_toshortside", t_RectAnti_toshortside, "rectangle anti-pad, space of signal via center to short side") )
elif t_ShapeAntipad == "2" :  #circle anti
	local_variable_list.append( ("t_D_cirantipad", t_D_cirantipad, "circle anti-pad, circle anti-pad diameter") )
else :  # ellipsoid anti-pad
	local_variable_list.append( ("t_D_antipad", t_D_antipad, "ellipsoid anti-pad diameter") )

for i in local_variable_list :
	addlocalvariable( oDesign, i[0], i[1], i[2] )
	exec( i[0] + "=" + "\"" + i[0]  + "\"" )

##### ------++--- project --+++---
	
# __00___ input value process and check the value

#
t_Lsize = [t_Lsize_x, t_Lsize_y]    # [x,y] , PCB block size

n_startlayer = int(t_startlayer)
n_endlayer = int(t_endlayer)
n_backdrill_top = int(t_backdrill_top)
n_backdrill_bottom = int(t_backdrill_bottom)

Ttotalthick = "0mil"        # not include solder layer
for i in t_Tpcb_list[1:-1] :
	Ttotalthick = Ttotalthick + "+" + i

n_totallayers = (len( t_Tpcb_list[1:-1] )+1)/2
#

# check stackup info
if not len( t_Layertype ) == len( t_Tpcb_list ) == len( t_PP_dk ) == len( t_PP_df ) :
	oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- stackup info error")
# check layer type
CheckLayerType = [ ( i.lower() in ["plane","gnd","pwr","power","p","ground"] ) for i in t_Layertype ]
if ( True not in CheckLayerType ) :
	oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- layer type error, no plane layer")	
if ( t_Layertype[n_startlayer*2-1].lower() not in ["signal","sig"] ) or ( t_Layertype[n_endlayer*2-1].lower() not in ["signal","sig"] ) :
	oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- layer type error")
# check backdrill layer info
if backdrillornot :
	if not ( (min(n_backdrill_top,n_backdrill_bottom) <= n_startlayer <= max(n_backdrill_top,n_backdrill_bottom)) and (min(n_backdrill_top,n_backdrill_bottom) <= n_endlayer <= max(n_backdrill_top,n_backdrill_bottom)) ) :
		oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- backdrill info or trace layer error")
# check signal layer info
if n_startlayer == n_endlayer :
	oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- trace layer error")
# check soldermask layer info
if ( t_Layertype[0].lower() not in ["sm", "solder", "soldermask"] ) or ( t_Layertype[-1].lower() not in ["sm", "solder", "soldermask"] ) :
	oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- no solder mask layer ")

# __00___ check input value

# __01___ material and color list
MaterialList = []   # include PP and cppper
PPMaterialList = []  # just pp
PP_Material_layer = []   # include solder layer
for i,v in enumerate(t_PP_dk) :
	PP_Material_layer.append( ("PP_" + v + "_" + t_PP_df[i] ).replace(".","d") )
MaterialList = list(set(PP_Material_layer))   # ['PP_4d1_0d025', 'PP_4_0d025', 'PP_3d4_0d045'] 
PPMaterialList = list(set(PP_Material_layer)) # ['PP_4d1_0d025', 'PP_4_0d025', 'PP_3d4_0d045'] 
MaterialList.append("Copper_5d8E7")           # add "Copper_5d8E7"

MaterialColor = {}
Materialcolor_layer = []  # include solder layer
for i,v in enumerate( MaterialList ) :
	if v != "Copper_5d8E7" :
		MaterialColor[v] = str( (0, 220 - int( (220-100)/len(MaterialList) )*i, 0) )    # solder_color = "(0, 255, 0)"
	MaterialColor["Copper_5d8E7"] = "(240, 240, 0)"  # copper color 
for i in PP_Material_layer :
	Materialcolor_layer.append( MaterialColor[i] )
# __01___ material and color list

# __02___ add new material (include pp and copper)
oDefinitionManager = oProject.GetDefinitionManager()

for i in MaterialList :
	if i != "Copper_5d8E7" :
		j = i.split("_")
		j_dk = j[1].replace("d", ".")   # '4.0'
		j_df = j[2].replace("d", ".")   # '0.025'	
		addmaterial(oDefinitionManager, i, j_dk, j_df)
	else :
		addmaterial(oDefinitionManager, i, "0.999991", "5.8E7")
# __02___ add new material

# __03__ stackup
Tthick = "0mil"
for i,v in enumerate( t_Tpcb_list[1:-1] ) :   # t_Tpcb_list = ["0.6mil"  , "1.89mil" , "2.75mil" , "1.18mil" , ... , "1.89mil" , "0.6mil" ]
	creatbox(oEditor, t_Lsize[0]+ "/2*(-1)",  t_Lsize[1]+ "/2*(-1)", Tthick, \
			t_Lsize[0], t_Lsize[1], v, \
			"PP_" + "{:0>3}".format(i), Materialcolor_layer[1:-1][i], 0.7, PP_Material_layer[1:-1][i])
	Tthick = Tthick + "+" + v   # sum thick
# __03__ stackup

# __04__ signal via Cylinder
layer_shapepad = []
for i,v in enumerate( t_Tpcb_list[1:-1] ) :
	if i == 0 or i == len( t_Tpcb_list[1:-1] ) - 1 or i == (n_startlayer-1)*2 or i == (n_endlayer-1)*2 :
		layer_shapepad.append( t_D_pad )
	else :
		layer_shapepad.append( t_D_drill )

Tthick = "0mil"
for i,v in enumerate( t_Tpcb_list[1:-1] ) :
	createcylinder(oEditor, t_Space_via2via + "/2", "0mil", Tthick, \
			layer_shapepad[i] + "/2", v, \
			"sig_paddrill_" + "{:0>3}".format(i) + "_p", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")
	createcylinder(oEditor, t_Space_via2via + "/2*(-1)", "0mil", Tthick, \
			layer_shapepad[i] + "/2*(-1)", v, \
			"sig_paddrill_" + "{:0>3}".format(i) + "_n", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")	
	Tthick = Tthick + "+" + v   # sum thick
# __04__ signal via Cylinder

# __05___ Ref (GND) structure , gnd via(not annular) and gnd plane(with void) 
layer_RefStructure = []
for i,v in enumerate( t_Layertype[1:-1] ) :
	if ( i == 0 or i == len( t_Layertype[1:-1] )-1 ) and ( v.lower() not in ["plane","gnd","pwr","power","p","ground"] ) :
		layer_RefStructure.append("refpad")
	elif v.lower() in ["plane","gnd","pwr","power","p","ground"] :
		layer_RefStructure.append("refplane")
	else :
		layer_RefStructure.append("refdrill")

## ref via position  [x,y]
refviaposition_p = [ t_Space_via2via + "/2" + "+" + "sin(" + p_RefViatoYaxis_Angle + ")*" + p_RefViatoSigVia_Distance, \
					"cos(" + p_RefViatoYaxis_Angle + ")*" + p_RefViatoSigVia_Distance ]     
refviaposition_n = [ t_Space_via2via + "/2" + "*(-1)" + "+" + "sin(" + n_RefViatoYaxis_Angle + ")*" + n_RefViatoSigVia_Distance + "*(-1)", \
					"cos(" + n_RefViatoYaxis_Angle + ")*" + n_RefViatoSigVia_Distance ] 

Tthick = "0mil"
for i,v in enumerate( t_Tpcb_list[1:-1] ) :
	if layer_RefStructure[i] == "refpad" :
		createcylinder(oEditor, refviaposition_p[0], refviaposition_p[1], Tthick, \
				t_D_pad + "/2", v, \
				"ref_" + "{:0>3}".format(i) + "_p", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")	
		createcylinder(oEditor, refviaposition_n[0], refviaposition_n[1], Tthick, \
				t_D_pad + "/2", v, \
				"ref_" + "{:0>3}".format(i) + "_n", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")	
	elif layer_RefStructure[i] == "refdrill" :
		createcylinder(oEditor, refviaposition_p[0], refviaposition_p[1], Tthick, \
				t_D_drill + "/2", v, \
				"ref_" + "{:0>3}".format(i) + "_p", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")	
		createcylinder(oEditor, refviaposition_n[0], refviaposition_n[1], Tthick, \
				t_D_drill + "/2", v, \
				"ref_" + "{:0>3}".format(i) + "_n", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")	
	else :
		creatbox(oEditor, t_Lsize[0]+ "/2*(-1)",  t_Lsize[1]+ "/2*(-1)", Tthick, \
				t_Lsize[0], t_Lsize[1], v, \
				"ref_" + "{:0>3}".format(i), MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7")	
		# void from plane
		if t_ShapeAntipad == "1" :  #rect anti
			rectangle_voidstruct( oEditor , t_Space_via2via , t_RectAnti_toLongside, t_RectAnti_toshortside, Tthick, v, "refvoid_" + "{:0>3}".format(i)  )
			subtract(oEditor, "ref_" + "{:0>3}".format(i), ["refvoid_" + "{:0>3}".format(i)], False)
		elif t_ShapeAntipad == "2" :  #circle anti
			circle_voidstruct( oEditor , t_Space_via2via , t_D_cirantipad , Tthick, v, "refvoid_" + "{:0>3}".format(i) )
			subtract(oEditor, "ref_" + "{:0>3}".format(i), ["refvoid_" + "{:0>3}".format(i) + "_Pvoid_cir", "refvoid_" + "{:0>3}".format(i) + "_Nvoid_cir"], False)
		else :  # ellipsoid anti
			ellipsoid_voidstruct( oEditor , t_Space_via2via , t_D_antipad , Tthick, v, "refvoid_" + "{:0>3}".format(i) )
			subtract(oEditor, "ref_" + "{:0>3}".format(i), ["refvoid_" + "{:0>3}".format(i)], False)
		
	Tthick = Tthick + "+" + v   # sum thick	
# __05___ Ref (GND) structure

# __06__ add signal trace
# startlayer endlayer
layer_trace = []
for i,v in enumerate( t_Tpcb_list[1:-1] ) :
	if i == (n_startlayer - 1)*2 :
		layer_trace.append("startlayer")
	elif i == (n_endlayer - 1)*2 :
		layer_trace.append("endlayer")
	else :
		layer_trace.append(False)

# trace 
x1 = "(" + t_W_trace + "+" + t_S_trace + ")" + "/2"
y1 = "(" + t_Lsize[1] + ")" + "/2"
x2 = "(" + t_W_trace + "+" + t_S_trace + ")" + "/2"
y2 = "(" + t_Space_via2via + "-" + t_W_trace + "-" + t_S_trace + ")" + "/2"
x3 = "(" + t_Space_via2via + "-" + t_D_drill + "/sqrt(2)" + ")" + "/2"
y3 = "(" + t_D_drill + "/sqrt(2)" + ")" + "/2"
		
Tthick = "0mil"
for i,v in enumerate( t_Tpcb_list[1:-1] ) :
	if layer_trace[i] == "startlayer" :
		addrecttrace( oEditor, [ t_S_trace + "/2", y1, Tthick ],\
					[ v, t_W_trace ], [ ( x1, y1, Tthick), ( x2, y2, Tthick), ( x3, y3, Tthick) ],\
					"sig_trace_" + "{:0>3}".format(i) + "_p", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7") 
		addrecttrace( oEditor, [ t_S_trace + "/2*(-1)", y1, Tthick ],\
					[ v, t_W_trace + "*(-1)" ], [ ( x1 + "*(-1)", y1, Tthick), ( x2 + "*(-1)", y2, Tthick), ( x3 + "*(-1)", y3, Tthick) ],\
					"sig_trace_" + "{:0>3}".format(i) + "_n", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7") 		
	if layer_trace[i] == "endlayer" :
		addrecttrace( oEditor, [ t_S_trace + "/2", y1 + "*(-1)", Tthick ],\
					[ v, t_W_trace ], [ ( x1, y1 + "*(-1)", Tthick), ( x2, y2 + "*(-1)", Tthick), ( x3, y3 + "*(-1)", Tthick) ],\
					"sig_trace_" + "{:0>3}".format(i) + "_p", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7") 
		addrecttrace( oEditor, [ t_S_trace + "/2*(-1)",  y1 + "*(-1)", Tthick ],\
					[ v, t_W_trace + "*(-1)" ], [ ( x1 + "*(-1)", y1 + "*(-1)", Tthick), ( x2 + "*(-1)", y2 + "*(-1)", Tthick), ( x3 + "*(-1)", y3 + "*(-1)", Tthick) ],\
					"sig_trace_" + "{:0>3}".format(i) + "_n", MaterialColor["Copper_5d8E7"], 0, "Copper_5d8E7") 	
		
	Tthick = Tthick + "+" + v   # sum thick	
# __06__ add signal trace

# __07__ processing struct
# Subtract
Lstructinlayer = []
for i,v in enumerate( t_Tpcb_list[1:-1] ) :
	Lstructinlayer = oEditor.GetMatchedObjectName( "*_" + "{:0>3}".format(i)+"*" )
	Lstructinlayer.remove( "PP_" + "{:0>3}".format(i) )
	
	subtract( oEditor, "PP_" + "{:0>3}".format(i), Lstructinlayer, True)
# Unite
keywordstruct = ["ref_*", "sig_*_n", "sig_*_p"]
newstructname = ["RefStruct", "Sig_n", "Sig_p"]
for i,v in enumerate( keywordstruct ) :
	structinlayer = oEditor.GetMatchedObjectName( v )
	
	unite( oEditor, structinlayer, False )	

	oEditor.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:Geometry3DAttributeTab",
				[
					"NAME:PropServers", 
					structinlayer[0]
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:Name",
						"Value:="		, newstructname[i]
					]
				]
			]
		])
# __07__ processing struct	

# __08__ ref drill

# ref void
createcylinder(oEditor, refviaposition_p[0], refviaposition_p[1], "0mil", \
		t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Ttotalthick, \
		"ref_void_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )	
createcylinder(oEditor, refviaposition_n[0], refviaposition_n[1], "0mil", \
		t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Ttotalthick, \
		"ref_void_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )	
subtract( oEditor, "RefStruct", ["ref_void_p", "ref_void_n"], True )
	
# __08__ ref drill

# __09__ soldermask layer
# up pad refviaposition_p[0], refviaposition_p[1]
L_solderuptrace_info = \
[( "sm_pad_reftop_p", refviaposition_p[0], refviaposition_p[1] , t_Tpcb_list[0] + "*(-1)" ) , \
( "sm_pad_sigtop_p", t_Space_via2via + "/2", "0mil" , t_Tpcb_list[0] + "*(-1)" ) , \
( "sm_pad_reftop_n",  refviaposition_n[0], refviaposition_n[1] , t_Tpcb_list[0] + "*(-1)" ) , \
( "sm_pad_sigtop_n", t_Space_via2via + "/2*(-1)", "0mil" , t_Tpcb_list[0] + "*(-1)" ) , \
( "sm_pad_refbtm_p", refviaposition_p[0], refviaposition_p[1] , t_Tpcb_list[0] ) , \
( "sm_pad_sigbtm_p", t_Space_via2via + "/2", "0mil" , t_Tpcb_list[0] ) , \
( "sm_pad_refbtm_n",  refviaposition_n[0], refviaposition_n[1] , t_Tpcb_list[0] ) , \
( "sm_pad_sigbtm_n", t_Space_via2via + "/2*(-1)", "0mil" , t_Tpcb_list[0] ) ]

for i in L_solderuptrace_info:
	if "top" in i[0]:
		createcylinder(oEditor, i[1], i[2], "0mil", \
				t_D_pad + "/2" + "+" + t_Tpcb_list[0], i[3], \
				i[0], Materialcolor_layer[0], 0.7, PP_Material_layer[0] )
	else :
		createcylinder(oEditor, i[1], i[2], Ttotalthick, \
				t_D_pad + "/2" + "+" + t_Tpcb_list[0], i[3], \
				i[0], Materialcolor_layer[0], 0.7, PP_Material_layer[0] )
				
# up trace
# if startlayer/endlayer is top or bottom, add solder on trace
if n_startlayer == 1 :
	# # LCrossSectionXYZ_t -> [x,y,z] ; LWandH_t -> [w,h] ; Lpath_3pXYZ -> [(x0,y0,z0),(x1,y1,z1),(x2,y2,z2)]
	# addrecttrace( oEditor, LCrossSectionXYZ_t, LWandH_t, Lpath_3pXYZ, Tname, Tcolor, Num_trans, Tmate)
	addrecttrace( oEditor, [ t_S_trace + "/2" + "+" + t_Tpcb_list[0] + "*(-1)" , y1, "0mil" ],\
				[ t_Tpcb_list[0] + "*(-1)", t_W_trace + "+" + t_Tpcb_list[0] + "*2" ], [ ( x1, y1, "0mil"), ( x2, y2, "0mil"), ( x3, y3, "0mil") ],\
				"sm_trace_sigtop_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 
	addrecttrace( oEditor, [ t_S_trace + "/2" + "*(-1)" + "+" + t_Tpcb_list[0]  , y1, "0mil"],\
				[ t_Tpcb_list[0] + "*(-1)", t_W_trace + "*(-1)" + "+" + t_Tpcb_list[0] + "*(-1)" + "*2" ], [ ( x1 + "*(-1)", y1, "0mil"), ( x2 + "*(-1)", y2, "0mil"), ( x3 + "*(-1)", y3, "0mil") ],\
				"sm_trace_sigtop_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0])
elif n_startlayer == n_totallayers :
	addrecttrace( oEditor, [ t_S_trace + "/2" + "+" + t_Tpcb_list[0] + "*(-1)" , y1, Ttotalthick ],\
				[ t_Tpcb_list[0] , t_W_trace + "+" + t_Tpcb_list[0] + "*2" ], [ ( x1, y1, Ttotalthick), ( x2, y2, Ttotalthick), ( x3, y3, Ttotalthick) ],\
				"sm_trace_sigbtm_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 
	addrecttrace( oEditor, [ t_S_trace + "/2" + "*(-1)" + "+" + t_Tpcb_list[0] , y1, Ttotalthick ],\
				[ t_Tpcb_list[0] , t_W_trace + "*(-1)" + "+" + t_Tpcb_list[0] + "*(-1)" + "*2" ], [ ( x1 + "*(-1)", y1, Ttotalthick), ( x2 + "*(-1)", y2, Ttotalthick), ( x3 + "*(-1)", y3, Ttotalthick) ],\
				"sm_trace_sigbtm_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 				

if n_endlayer == 1 :
	addrecttrace( oEditor, [ t_S_trace + "/2" + "+" + t_Tpcb_list[0] + "*(-1)" , y1 + "*(-1)", "0mil" ],\
				[ t_Tpcb_list[0] + "*(-1)" , t_W_trace + "+" + t_Tpcb_list[0] + "*2" ], [ ( x1, y1 + "*(-1)", "0mil"), ( x2, y2 + "*(-1)", "0mil"), ( x3, y3 + "*(-1)", "0mil") ],\
				"sm_trace2_sigtop_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 
	addrecttrace( oEditor, [ t_S_trace + "/2" + "*(-1)" + "+" + t_Tpcb_list[0] , y1 + "*(-1)", "0mil" ],\
				[ t_Tpcb_list[0] + "*(-1)" , t_W_trace + "*(-1)" + "+" + t_Tpcb_list[0] + "*(-1)" + "*2" ], [ ( x1 + "*(-1)", y1 + "*(-1)", "0mil"), ( x2 + "*(-1)", y2 + "*(-1)", "0mil"), ( x3 + "*(-1)", y3 + "*(-1)", "0mil") ],\
				"sm_trace2_sigtop_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 				
elif n_endlayer == n_totallayers :
	addrecttrace( oEditor, [ t_S_trace + "/2" + "+" + t_Tpcb_list[0] + "*(-1)" , y1 + "*(-1)", Ttotalthick ],\
				[ t_Tpcb_list[0] , t_W_trace + "+" + t_Tpcb_list[0] + "*2" ], [ ( x1, y1 + "*(-1)", Ttotalthick), ( x2, y2 + "*(-1)", Ttotalthick), ( x3, y3 + "*(-1)", Ttotalthick) ],\
				"sm_trace2_sigbtm_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 
	addrecttrace( oEditor, [ t_S_trace + "/2" + "*(-1)" + "+" + t_Tpcb_list[0] , y1 + "*(-1)", Ttotalthick ],\
				[ t_Tpcb_list[0] , t_W_trace + "*(-1)" + "+" + t_Tpcb_list[0] + "*(-1)" + "*2" ], [ ( x1 + "*(-1)", y1 + "*(-1)", Ttotalthick), ( x2 + "*(-1)", y2 + "*(-1)", Ttotalthick), ( x3 + "*(-1)", y3 + "*(-1)", Ttotalthick) ],\
				"sm_trace2_sigbtm_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0]) 

# __09__ soldermask layer

# __10__ sig drill
if backdrillornot :   # with backdrill
	if ( ( n_totallayers in [ n_backdrill_top , n_backdrill_bottom ] ) and ( 1 not in [ n_backdrill_top , n_backdrill_bottom ] ) ) or ( ( n_totallayers not in [ n_backdrill_top , n_backdrill_bottom ] ) and ( 1 in [ n_backdrill_top , n_backdrill_bottom ] ) ):
		
		if 1 in [ n_backdrill_top , n_backdrill_bottom ] :
		
			n_backdrillendlayer = max( n_backdrill_top , n_backdrill_bottom )
			Tvoidthick1 = "0mil"
			for i in t_Tpcb_list[1:-1][0:(n_backdrillendlayer * 2 - 1)] :
				Tvoidthick1 = Tvoidthick1 + "+" + i
			Tvoidthick1 = Tvoidthick1 + "+" + t_backdrill_stub
			
			# createcylinder(obj, xP, yP, zP, Rradius, Lheight, Tname, Tcolor, Num_trans, Tmate)
			createcylinder(oEditor, t_Space_via2via + "/2" , "0mil", "0mil", \
					t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Tvoidthick1 , \
					"sig_void_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )			
			createcylinder(oEditor, t_Space_via2via + "/2" + "*(-1)" , "0mil", "0mil", \
					t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Tvoidthick1 , \
					"sig_void_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )			
			
			# subtract(obj, Tblankpart, Ltoolpart, Bool_KeepOriginal)
			subtract(oEditor, "Sig_n", ["sig_void_n"], True)
			subtract(oEditor, "Sig_p", ["sig_void_p"], True)
			
		else :        
			n_backdrillstartlayer = min( n_backdrill_top , n_backdrill_bottom )
			Tvoidthick2 = "0mil"
			for i in t_Tpcb_list[1:-1][((n_backdrillstartlayer - 1) * 2) ::] :
				Tvoidthick2 = Tvoidthick2 + "+" + i + "*(-1)"
			Tvoidthick2 = Tvoidthick2 + "+" + t_backdrill_stub + "*(-1)"			
			
			createcylinder(oEditor, t_Space_via2via + "/2" , "0mil", Ttotalthick, \
					t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Tvoidthick2 , \
					"sig_void_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )				
			createcylinder(oEditor, t_Space_via2via + "/2" + "*(-1)" , "0mil", Ttotalthick, \
					t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Tvoidthick2 , \
					"sig_void_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )			
			
			subtract(oEditor, "Sig_n", ["sig_void_n"], True)
			subtract(oEditor, "Sig_p", ["sig_void_p"], True)					
		
	else :
		oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- backdrill info error")
else :  # without backdrill
	createcylinder(oEditor, t_Space_via2via + "/2" , "0mil", "0mil", \
			t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Ttotalthick , \
			"sig_void_p", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )	
	createcylinder(oEditor, t_Space_via2via + "/2" + "*(-1)" , "0mil", "0mil", \
			t_D_drill + "/2" + "+" + t_Tplating + "*(-1)", Ttotalthick , \
			"sig_void_n", Materialcolor_layer[0], 0.7, PP_Material_layer[0] )	
	subtract(oEditor, "Sig_n", ["sig_void_n"], True)
	subtract(oEditor, "Sig_p", ["sig_void_p"], True)	

# __10__ sig drill

# __11____ process struct 2

for i in PPMaterialList :
	ppstructs = oEditor.GetObjectsByMaterial( i )
	
	unite( oEditor, ppstructs, False )
			
	oEditor.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:Geometry3DAttributeTab",
				[
					"NAME:PropServers", 
					ppstructs[0]
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:Name",
						"Value:="		, i + "_Struct"
					]
				]
			]
		])		
			
# __11____ process struct 2

# __12____ backdrill

allsolids_structs_back = oEditor.GetObjectsInGroup( "Solids" )
blankparts_backdrill = allsolids_structs_back[0]
for a,b in enumerate( allsolids_structs_back ) :
	if a>0 :
		blankparts_backdrill += ("," + b)

if backdrillornot :   # with backdrill
	if ( ( n_totallayers in [ n_backdrill_top , n_backdrill_bottom ] ) and ( 1 not in [ n_backdrill_top , n_backdrill_bottom ] ) ) or ( ( n_totallayers not in [ n_backdrill_top , n_backdrill_bottom ] ) and ( 1 in [ n_backdrill_top , n_backdrill_bottom ] ) ):
		
		if 1 in [ n_backdrill_top , n_backdrill_bottom ] :
		
			n_backdrillendlayer = max( n_backdrill_top , n_backdrill_bottom )
			Theight_backdrill = Ttotalthick
			for i in t_Tpcb_list[1:-1][0:(n_backdrillendlayer * 2 - 1)] :
				Theight_backdrill = Theight_backdrill + "+" + i + "*(-1)"
			Theight_backdrill = Theight_backdrill + "+" + t_backdrill_stub + "*(-1)" + "+" + t_Tpcb_list[0]
			
			createcylinder(oEditor, t_Space_via2via + "/2" , "0mil", Ttotalthick + "+" + t_Tpcb_list[0], \
					t_D_backdrill + "/2" , "(" + Theight_backdrill + ")" + "*(-1)", \
					"sig_backdrill_p", "(143 175 143)", 0, "vacuum" )					
			createcylinder(oEditor, t_Space_via2via + "/2" + "*(-1)" , "0mil", Ttotalthick + "+" + t_Tpcb_list[0], \
					t_D_backdrill + "/2" , "(" + Theight_backdrill + ")" + "*(-1)", \
					"sig_backdrill_n", "(143 175 143)", 0, "vacuum" )					
			subtract(oEditor, blankparts_backdrill, ["sig_backdrill_p", "sig_backdrill_n"], False)
			
		else :        # totallayernum in [ backdrill_top , backdrill_bottom ]
			n_backdrillstartlayer = min( n_backdrill_top , n_backdrill_bottom )
			Theight_backdrill = Ttotalthick
			for i in t_Tpcb_list[1:-1][((n_backdrillstartlayer - 1) * 2) ::] :
				Theight_backdrill = Theight_backdrill + "+" + i + "*(-1)"
			Theight_backdrill = Theight_backdrill + "+" + t_backdrill_stub + "*(-1)" + "+" + t_Tpcb_list[0]		

			createcylinder(oEditor, t_Space_via2via + "/2" , "0mil", t_Tpcb_list[0] + "*(-1)", \
					t_D_backdrill + "/2" , Theight_backdrill , \
					"sig_backdrill_p", "(143 175 143)", 0, "vacuum" )				
			createcylinder(oEditor, t_Space_via2via + "/2" + "*(-1)" , "0mil", t_Tpcb_list[0] + "*(-1)", \
					t_D_backdrill + "/2" , Theight_backdrill , \
					"sig_backdrill_n", "(143 175 143)", 0, "vacuum" )			
			subtract(oEditor, blankparts_backdrill, ["sig_backdrill_p", "sig_backdrill_n"], False)			
			
	else :
		oDesktop.AddMessage("", "", 2, "DiffViaPyfile --- backdrill info error")

# __12____ backdrill

# __13____ add diff wave port
# step1 add sheet
# if trace is Microstrip line     
if n_startlayer == 1 :  # Microstrip

	TportZp = "0mil"
	for i,v in enumerate( t_Layertype[1:-1] ) :
		if v.lower() not in ["plane","gnd","pwr","power","p","ground"] :
			TportZp = TportZp + "+" + t_Tpcb_list[1:-1][i]
		else :
			break

	# addrect( oEditor, LCrossSectionXYZ_t, LWandH_t, Tname, Tcolor, Num_trans, Tmate)
	addrect( oEditor, [ t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize , t_Lsize[1] + "/2", TportZp ],\
			[ t_Tpcb_list[2] + "*" + MsPortYsize + "*(-1)", "(" + t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize + ")" + "*2" + "*(-1)" ], \
			"Diffport_1", "(140 140 140)", 0.5, "vacuum" )
			
elif n_startlayer == n_totallayers :   # Microstrip

	TportZp_ = "0mil"
	for i,v in enumerate( t_Layertype[1:-1][::-1] ) :
		if v.lower() not in ["plane","gnd","pwr","power","p","ground"] :
			TportZp_ = TportZp_ + "+" + t_Tpcb_list[1:-1][::-1][i]
		else :
			break
			
	addrect( oEditor, [ t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize , t_Lsize[1] + "/2", Ttotalthick + "+" + "(" + TportZp_ + ")" + "*(-1)" ],\
			[ t_Tpcb_list[2] + "*" + MsPortYsize, "(" + t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize + ")" + "*2" + "*(-1)" ], \
			"Diffport_1", "(140 140 140)", 0.5, "vacuum" )
else :  # stripline
	boolPlaneLayer = [ ( i.lower() in ["plane","gnd","pwr","power","p","ground"] ) for i in t_Layertype[1:-1] ]
	# [False, False, False, True, False, False, False, False, False, True, False, False, False]
	Nplanelayerindex = []
	for i,v in enumerate( boolPlaneLayer ) :
		if v :
			Nplanelayerindex.append(i)
	Nplanelayerindex.append( ( n_startlayer - 1 ) * 2 )
	Nplanelayerindex.sort()	
	# [3, 4, 9]
	n_index = Nplanelayerindex.index( ( n_startlayer - 1 ) * 2 )
	# 
	TportZp_2 = "0mil"
	for i in t_Tpcb_list[1:-1][:( Nplanelayerindex[ n_index-1 ] + 1 )] :
		TportZp_2 = TportZp_2 + "+" + i
	
	TportH_ = "0mil"
	for i in t_Tpcb_list[1:-1][( Nplanelayerindex[ n_index-1 ] + 1 ):( Nplanelayerindex[ n_index+1 ] )] :
		TportH_ = TportH_ + "+" + i

	addrect( oEditor, [ t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + SlPortXsize , t_Lsize[1] + "/2", TportZp_2 ],\
			[ TportH_, "(" + t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + SlPortXsize + ")" + "*2" + "*(-1)" ], \
			"Diffport_1", "(140 140 140)", 0.5, "vacuum" )
	
if n_endlayer == 1 :
	TportZp = "0mil"
	for i,v in enumerate( t_Layertype[1:-1] ) :
		if v.lower() not in ["plane","gnd","pwr","power","p","ground"] :
			TportZp = TportZp + "+" + t_Tpcb_list[1:-1][i]
		else :
			break
	addrect( oEditor, [ t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize , t_Lsize[1] + "/2" + "*(-1)", TportZp ],\
			[ t_Tpcb_list[2] + "*" + MsPortYsize + "*(-1)", "(" + t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize + ")" + "*2" + "*(-1)" ], \
			"Diffport_2", "(140 140 140)", 0.5, "vacuum" )				
elif n_endlayer == n_totallayers :
	TportZp_ = "0mil"
	for i,v in enumerate( t_Layertype[1:-1][::-1] ) :
		if v.lower() not in ["plane","gnd","pwr","power","p","ground"] :
			TportZp_ = TportZp_ + "+" + t_Tpcb_list[1:-1][::-1][i]
		else :
			break
	addrect( oEditor, [ t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize , t_Lsize[1] + "/2" + "*(-1)", Ttotalthick + "+" + "(" + TportZp_ + ")" + "*(-1)" ],\
			[ t_Tpcb_list[2] + "*" + MsPortYsize, "(" + t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + MsPortXsize + ")" + "*2" + "*(-1)" ], \
			"Diffport_2", "(140 140 140)", 0.5, "vacuum" )
else :
	boolPlaneLayer = [ ( i.lower() in ["plane","gnd","pwr","power","p","ground"] ) for i in t_Layertype[1:-1] ]
	# [False, False, False, True, False, False, False, False, False, True, False, False, False]
	Nplanelayerindex = []
	for i,v in enumerate( boolPlaneLayer ) :
		if v :
			Nplanelayerindex.append(i)
	Nplanelayerindex.append( ( n_endlayer - 1 ) * 2 )
	Nplanelayerindex.sort()	
	# [3, 4, 9]
	n_index = Nplanelayerindex.index( ( n_endlayer - 1 ) * 2 )
	# 
	TportZp_2 = "0mil"
	for i in t_Tpcb_list[1:-1][:( Nplanelayerindex[ n_index-1 ] + 1 )] :
		TportZp_2 = TportZp_2 + "+" + i
	
	TportH_ = "0mil"
	for i in t_Tpcb_list[1:-1][( Nplanelayerindex[ n_index-1 ] + 1 ):( Nplanelayerindex[ n_index+1 ] )] :
		TportH_ = TportH_ + "+" + i

	addrect( oEditor, [ t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + SlPortXsize , t_Lsize[1] + "/2" + "*(-1)", TportZp_2 ],\
			[ TportH_, "(" + t_S_trace + "/2" + "+" + t_W_trace + "+" + t_W_trace + "*" + SlPortXsize + ")" + "*2" + "*(-1)" ], \
			"Diffport_2", "(140 140 140)", 0.5, "vacuum" )

# step2 Identify Port
oModule = oDesign.GetModule("BoundarySetup")
oModule.AutoIdentifyPorts(
	[
		"NAME:Faces", 
		int( oEditor.GetFaceIDs("Diffport_1")[0] )
	], True, 
	[
		"NAME:ReferenceConductors", 
		"RefStruct"
	], "Diffport_startlayer", True)
oModule.AutoIdentifyPorts(
	[
		"NAME:Faces", 
		int( oEditor.GetFaceIDs("Diffport_2")[0] )
	], True, 
	[
		"NAME:ReferenceConductors", 
		"RefStruct"
	], "Diffport_endlayer", True)
# __13____ add diff wave port

# __14____ airbox
if n_startlayer == 1 or n_startlayer == n_totallayers or n_endlayer == 1 or n_endlayer == n_totallayers :
	creatbox(oEditor, t_Lsize[0] + "/2" + "*(-1)", t_Lsize[1] + "/2" + "*(-1)", "max(" + AirBoxHSizeaboveTOP + ", " + t_Tpcb_list[2] + "*" + MsPortYsize + ")" + "*(-1)", \
		t_Lsize[0], t_Lsize[1], "max(" + AirBoxHSizeaboveTOP + ", " + t_Tpcb_list[2] + "*" + MsPortYsize + ")" + "*2" + "+" + Ttotalthick, \
		"AirBox", "(220 220 220)", 1, "air")
else :
	creatbox(oEditor, t_Lsize[0] + "/2" + "*(-1)", t_Lsize[1] + "/2" + "*(-1)", AirBoxHSizeaboveTOP + "*(-1)", \
		t_Lsize[0], t_Lsize[1], AirBoxHSizeaboveTOP + "*2" + "+" + Ttotalthick, \
		"AirBox", "(220 220 220)", 1, "air")
# oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignRadiation(
	[
		"NAME:AirBox",
		"Objects:="		, ["AirBox"],
		"IsFssReference:="	, False,
		"IsForPML:="		, False
	])
# __14____ airbox

# __15___ analysis setup
oModule = oDesign.GetModule("AnalysisSetup")
# add solution
oModule.InsertSetup("HfssDriven", 
	[
		"NAME:Setup1",
		"AdaptMultipleFreqs:="	, False,
		"Frequency:="		, Fsolution,
		"MaxDeltaS:="		, 0.01,
		"PortsOnly:="		, False,
		"UseMatrixConv:="	, False,
		"MaximumPasses:="	, 10,
		"MinimumPasses:="	, 1,
		"MinimumConvergedPasses:=", 2,
		"PercentRefinement:="	, 30,
		"IsEnabled:="		, True,
		"BasisOrder:="		, -1,
		"DoLambdaRefine:="	, True,
		"DoMaterialLambda:="	, True,
		"SetLambdaTarget:="	, False,
		"Target:="		, 0.6667,
		"UseMaxTetIncrease:="	, False,
		"PortAccuracy:="	, 2,
		"UseABCOnPort:="	, False,
		"SetPortMinMaxTri:="	, False,
		"UseDomains:="		, False,
		"UseIterativeSolver:="	, False,
		"SaveRadFieldsOnly:="	, False,
		"SaveAnyFields:="	, False,
		"IESolverType:="	, "Auto",
		"LambdaTargetForIESolver:=", 0.15,
		"UseDefaultLambdaTgtForIESolver:=", True,
		"RayDensityPerWavelength:=", 4,
		"MaxNumberOfBounces:="	, 5,
		"InfiniteSphereSetup:="	, -1
	])
# freq sweep
oModule.InsertFrequencySweep("Setup1", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "0GHz",
		"RangeEnd:="		, Fmax ,
		"RangeCount:="		, 2000,
		"Type:="		, "Interpolating",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"InterpTolerance:="	, 0.5,
		"InterpMaxSolns:="	, 250,
		"InterpMinSolns:="	, 0,
		"InterpMinSubranges:="	, 1,
		"ExtrapToDC:="		, True,
		"MinSolvedFreq:="	, "0.01GHz",
		"InterpUseS:="		, True,
		"InterpUsePortImped:="	, True,
		"InterpUsePropConst:="	, True,
		"UseDerivativeConvergence:=", False,
		"InterpDerivTolerance:=", 0.2,
		"UseFullBasis:="	, True,
		"EnforcePassivity:="	, True,
		"PassivityErrorTolerance:=", 0.0001,
		"EnforceCausality:="	, False
	])

# __15___ analysis setup

