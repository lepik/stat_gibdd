USE [DTP_KARD]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[CardDTP](
	[id_card_dtp] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
	[DTPV] [varchar](250) NULL,
	[date] [varchar](250) NULL,
	[district] [varchar](250) NULL,
	[KTS] [varchar](250) NULL,
	[KUCH] [varchar](250) NULL,
	[kartId] [varchar](250) NULL,
	[POG] [varchar](250) NULL,
	[RAN] [varchar](250) NULL,
	[rowNum] [varchar](250) NULL,
	[time] [varchar](250) NULL,
 CONSTRAINT [PK_CardDTP] PRIMARY KEY CLUSTERED 
(
	[id_card_dtp] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[CardDTP] ADD  CONSTRAINT [DF_CardDTP_id_card_dtp]  DEFAULT (newid()) FOR [id_card_dtp]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[InfoDTP](
	[id_info_dtp] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
	[id_card_dtp] [uniqueidentifier] NULL,
	[CHOM] [varchar](250) NULL,
	[COORD_L] [varchar](250) NULL,
	[COORD_W] [varchar](250) NULL,
	[dor] [varchar](250) NULL,
	[dor_k] [varchar](250) NULL,
	[dor_z] [varchar](250) NULL,
	[factor] [varchar](250) NULL,
	[house] [varchar](250) NULL,
	[k_ul] [varchar](250) NULL,
	[km] [varchar](250) NULL,
	[m] [varchar](250) NULL,
	[NP] [varchar](250) NULL,
	[ndu] [varchar](8000) NULL,
	[OBJ_DTP] [varchar](250) NULL,
	[osv] [varchar](250) NULL,
	[s_dtp] [varchar](250) NULL,
	[s_pch] [varchar](250) NULL,
	[sdor] [varchar](250) NULL,
	[spog] [varchar](250) NULL,
	[street] [varchar](250) NULL,
 CONSTRAINT [PK_InfoDTP] PRIMARY KEY CLUSTERED 
(
	[id_info_dtp] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[InfoDTP]  WITH CHECK ADD  CONSTRAINT [FK_InfoDTP_CardDTP] FOREIGN KEY([id_card_dtp])
REFERENCES [dbo].[CardDTP] ([id_card_dtp])
GO

ALTER TABLE [dbo].[InfoDTP] CHECK CONSTRAINT [FK_InfoDTP_CardDTP]
GO

ALTER TABLE [dbo].[InfoDTP] ADD  CONSTRAINT [DF_InfoDTP_id_info_dtp]  DEFAULT (newid()) FOR [id_info_dtp]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[InfoTs](
	[id_info_ts] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
	[id_info_dtp] [uniqueidentifier] NULL,
	[color] [varchar](250) NULL,
	[f_sob] [varchar](250) NULL,
	[g_v] [varchar](250) NULL,
	[m_pov] [varchar](8000) NULL,
	[m_ts] [varchar](250) NULL,
	[marka_ts] [varchar](250) NULL,
	[n_ts] [varchar](250) NULL,
	[o_pf] [varchar](250) NULL,
	[r_rul] [varchar](250) NULL,
	[t_n] [varchar](250) NULL,
	[t_ts] [varchar](250) NULL,
	[ts_s] [varchar](250) NULL,
 CONSTRAINT [PK_InfoTs] PRIMARY KEY CLUSTERED 
(
	[id_info_ts] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[InfoTs]  WITH CHECK ADD  CONSTRAINT [FK_InfoTs_InfoDTP] FOREIGN KEY([id_info_dtp])
REFERENCES [dbo].[InfoDTP] ([id_info_dtp])
GO

ALTER TABLE [dbo].[InfoTs] CHECK CONSTRAINT [FK_InfoTs_InfoDTP]
GO

ALTER TABLE [dbo].[InfoTs] ADD  CONSTRAINT [DF_InfoTs_id_info_ts]  DEFAULT (newid()) FOR [id_info_ts]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[InfoTsUchast](
	[id_info_ts_uch] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
	[id_info_ts] [uniqueidentifier] NULL,
	[ALCO] [varchar](250) NULL,
	[INJURED_CARD_ID] [varchar](250) NULL,
	[k_UCH] [varchar](250) NULL,
	[NPDD] [varchar](250) NULL,
	[n_UCH] [varchar](250) NULL,
	[POL] [varchar](250) NULL,
	[SAFETY_BELT] [varchar](250) NULL,
	[SOP_NPDD] [varchar](250) NULL,
	[s_SEAT_GROUP] [varchar](250) NULL,
	[s_SM] [varchar](250) NULL,
	[s_T] [varchar](250) NULL,
	[v_ST] [varchar](250) NULL,
 CONSTRAINT [PK_InfoTsUchast] PRIMARY KEY CLUSTERED 
(
	[id_info_ts_uch] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[InfoTsUchast]  WITH CHECK ADD  CONSTRAINT [FK_InfoTsUchast_InfoTs] FOREIGN KEY([id_info_ts])
REFERENCES [dbo].[InfoTs] ([id_info_ts])
GO

ALTER TABLE [dbo].[InfoTsUchast] CHECK CONSTRAINT [FK_InfoTsUchast_InfoTs]
GO

ALTER TABLE [dbo].[InfoTsUchast] ADD  CONSTRAINT [DF_InfoTsUchast_id_info_ts_uch]  DEFAULT (newid()) FOR [id_info_ts_uch]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[InfoUchast](
	[id_info_uch] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
	[id_info_dtp] [uniqueidentifier] NULL,
	[ALCO] [varchar](250) NULL,
	[k_UCH] [varchar](250) NULL,
	[NPDD] [varchar](250) NULL,
	[n_UCH] [varchar](250) NULL,
	[POL] [varchar](250) NULL,
	[SOP_NPDD] [varchar](250) NULL,
	[s_SM] [varchar](250) NULL,
	[s_T] [varchar](250) NULL,
	[v_ST] [varchar](250) NULL,
 CONSTRAINT [PK_InfoUchast] PRIMARY KEY CLUSTERED 
(
	[id_info_uch] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[InfoUchast]  WITH CHECK ADD  CONSTRAINT [FK_InfoUchast_InfoDTP] FOREIGN KEY([id_info_dtp])
REFERENCES [dbo].[InfoDTP] ([id_info_dtp])
GO

ALTER TABLE [dbo].[InfoUchast] CHECK CONSTRAINT [FK_InfoUchast_InfoDTP]
GO

ALTER TABLE [dbo].[InfoUchast] ADD  CONSTRAINT [DF_InfoUchast_id_info_uch]  DEFAULT (newid()) FOR [id_info_uch]
GO

