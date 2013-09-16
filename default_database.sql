/* Generacion de la base de datos vacia como destino de la informacion */

CREATE DATABASE base_ml;
--

\connect base_ml;
--

CREATE TABLE usuarios	(id_usuario int PRIMARY KEY,
						username varchar,
						ubicacion varchar,
						usuario_desde date,
						status varchar, 
						metadata_status varchar);
--

CREATE TABLE transacciones	(id_comprador int, 
							id_vendedor int,
							id_item int,
							calificacion varchar,
							fecha date,
							comentario varchar,
							monto float);
--

CREATE TABLE inventario_items	(id_item int,
								rubro varchar,
								monto float,
								link varchar);
--

INSERT INTO usuarios VALUES 	(61694482,
								'CAR_TECHNOLOGIES',
								'algunlugar',
								'1/1/2012',
								'pendiente');--
