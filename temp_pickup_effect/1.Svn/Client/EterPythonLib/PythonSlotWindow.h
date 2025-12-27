//Find
		ITEM_HEIGHT = 32,

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
		SLOT_ACTIVE_EFFECT_COUNT = 3,
#endif

//Find
	enum ESlotStyle
	{
		...
	};

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	enum ESlotColorType
	{
		COLOR_TYPE_ORANGE,
		COLOR_TYPE_WHITE,
		COLOR_TYPE_RED,
		COLOR_TYPE_GREEN,
		COLOR_TYPE_YELLOW,
		COLOR_TYPE_SKY,
		COLOR_TYPE_PINK,
	};
	
	enum ESlotHilight
	{
		HILIGHTSLOT_ACCE,
		HILIGHTSLOT_CHANGE_LOOK,
		HILIGHTSLOT_AURA,
		HILIGHTSLOT_CUBE,

		HILIGHTSLOT_MAX
	};
#endif

//Find
				CAniImageBox * pFinishCoolTimeEffect;

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
				D3DXCOLOR d3Color;
#endif

//Find
			void OnOverOutItem();

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
			void SetSlotDiffuseColor(DWORD dwIndex, int iColorType);
#endif

//Find
			void __CreateSlotEnableEffect();

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
			void __CreateSlotEnableEffect(int index);
#else
			void __CreateSlotEnableEffect();
#endif

//Find
			void __DestroySlotEnableEffect();

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
			void __DestroySlotEnableEffect(int index);
#else
			void __DestroySlotEnableEffect();
#endif

//Find
			CAniImageBox* m_pSlotActiveEffect;

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
			CAniImageBox * m_pSlotActiveEffect[SLOT_ACTIVE_EFFECT_COUNT];
#else
			CAniImageBox* m_pSlotActiveEffect;
#endif