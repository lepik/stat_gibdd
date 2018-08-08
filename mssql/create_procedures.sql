USE [DTP_KARD]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[Add_CardDTP](
	@id_card_dtp uniqueidentifier, 
	@DTPV varchar(250), 
	@date varchar(250), 
	@district varchar(250), 
	@KTS varchar(250), 
	@KUCH varchar(250), 
	@kartId varchar(250), 
	@POG varchar(250), 
	@RAN varchar(250), 
	@rowNum varchar(250), 
	@time varchar(250)
)
AS
BEGIN
 begin transaction
	INSERT INTO dbo.CardDTP(id_card_dtp, DTPV, [date], district, KTS, KUCH, kartId, POG, RAN, rowNum, [time])
	VALUES (@id_card_dtp, @DTPV, @date, @district, @KTS, @KUCH, @kartId, @POG, @RAN, @rowNum, @time)
 commit transaction
END

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[Add_InfoDTP](
	@id_info_dtp uniqueidentifier, 
	@id_card_dtp uniqueidentifier, 
	@CHOM varchar(250), 
	@COORD_L varchar(250), 
	@COORD_W varchar(250), 
	@dor varchar(250), 
	@dor_k varchar(250), 
	@dor_z varchar(250), 
	@factor varchar(250), 
	@house varchar(250), 
	@k_ul varchar(250), 
	@km varchar(250), 
	@m varchar(250), 
	@NP varchar(250), 
	@ndu varchar(8000), 
	@OBJ_DTP varchar(250), 
	@osv varchar(250), 
	@s_dtp varchar(250), 
	@s_pch varchar(250), 
	@sdor varchar(250), 
	@spog varchar(250), 
	@street varchar(250)
)
AS
BEGIN
 begin transaction
	INSERT INTO dbo.InfoDTP(id_info_dtp, id_card_dtp, CHOM, COORD_L, COORD_W, dor, dor_k, dor_z, factor, house, k_ul, km, m, NP, ndu, OBJ_DTP, osv, s_dtp, s_pch, sdor, spog, street)
	VALUES (@id_info_dtp, @id_card_dtp, @CHOM, @COORD_L, @COORD_W, @dor, @dor_k, @dor_z, @factor, @house, @k_ul, @km, @m, @NP, @ndu, @OBJ_DTP, @osv, @s_dtp, @s_pch, @sdor, @spog, @street)
 commit transaction
END

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[Add_InfoTS](
	@id_info_ts uniqueidentifier, 
	@id_info_dtp uniqueidentifier, 
	@color varchar(250), 
	@f_sob varchar(250),
	@g_v varchar(250), 
	@m_pov varchar(8000), 
	@m_ts varchar(250), 
	@marka_ts varchar(250), 
	@n_ts varchar(250), 
	@o_pf varchar(250), 
	@r_rul varchar(250), 
	@t_n varchar(250), 
	@t_ts varchar(250), 
	@ts_s varchar(250)
)
AS
BEGIN
 begin transaction
	INSERT INTO dbo.InfoTs(id_info_ts, id_info_dtp, color, f_sob, g_v, m_pov, m_ts, marka_ts, n_ts, o_pf, r_rul, t_n, t_ts, ts_s)
	VALUES (@id_info_ts, @id_info_dtp, @color, @f_sob, @g_v, @m_pov, @m_ts, @marka_ts, @n_ts, @o_pf, @r_rul, @t_n, @t_ts, @ts_s)
 commit transaction
END

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[Add_InfoTsUchast](	
	@id_info_ts_uch uniqueidentifier, 
	@id_info_ts uniqueidentifier,
	@ALCO varchar(250), 
	@INJURED_CARD_ID varchar(250), 
	@k_UCH varchar(250), 
	@NPDD varchar(250), 
	@n_UCH varchar(250), 
	@POL varchar(250), 
	@SAFETY_BELT varchar(250), 
	@SOP_NPDD varchar(250), 
	@s_SEAT_GROUP varchar(250), 
	@s_SM varchar(250), 
	@s_T varchar(250), 
	@v_ST varchar(250)
)
AS
BEGIN
 begin transaction
	INSERT INTO dbo.InfoTsUchast(id_info_ts_uch, id_info_ts, ALCO, INJURED_CARD_ID, k_UCH, NPDD, n_UCH, POL, SAFETY_BELT, SOP_NPDD, s_SEAT_GROUP, s_SM, s_T, v_ST)
	VALUES (@id_info_ts_uch, @id_info_ts, @ALCO, @INJURED_CARD_ID, @k_UCH, @NPDD, @n_UCH, @POL, @SAFETY_BELT, @SOP_NPDD, @s_SEAT_GROUP, @s_SM, @s_T, @v_ST)
 commit transaction
END

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[Add_InfoUchast](	
	@id_info_uch uniqueidentifier, 
	@id_info_dtp uniqueidentifier, 
	@ALCO varchar(250), 
	@k_UCH varchar(250), 
	@NPDD varchar(250), 
	@n_UCH varchar(250), 
	@POL varchar(250), 
	@SOP_NPDD varchar(250), 
	@s_SM varchar(250), 
	@s_T varchar(250), 
	@v_ST varchar(250)
)
AS
BEGIN
 begin transaction
	INSERT INTO dbo.InfoUchast(id_info_uch, id_info_dtp, ALCO, k_UCH, NPDD, n_UCH, POL, SOP_NPDD, s_SM, s_T, v_ST)
	VALUES (@id_info_uch, @id_info_dtp, @ALCO, @k_UCH, @NPDD, @n_UCH, @POL, @SOP_NPDD, @s_SM, @s_T, @v_ST)
 commit transaction
END

GO

