Estructura de archivos en results:

Encapsulado 1-4
	\_ A (rq) (curvas en directa de 0 V a 1 V para una cierta temperatura)
		\_ B.txt (para cada temperatura, hay muchas curvas IV. Contiene mediciones de V_sipm, I_sipm y R_rtd)
			
		\_ figures
			\_ B (iv).png (curvas IV correspondientes a las mediciones IV en B.txt)
			\_ B (res).png (R(time) correspondientes a las mediciones de R en B.txt)

	\_ A (vbr) (curvas en inversa de 0 V a 30 V para una cierta temperatura)
		\_ B.txt (para cada temperatura, hay muchas curvas IV. Contiene mediciones de V_sipm, I_sipm y R_rtd)
			
		\_ figures
			\_ B (iv).png (figuras correspondientes a las mediciones IV en B.txt)
			\_ B (res).png (figuras correspondientes a las mediciones de R en B.txt)


A y B son números enteros.
A corre desde 1 hasta el número de temperaturas distintas estudiadas
B corre desde 1 hasta el número de curvas IV que se miden por temperatura