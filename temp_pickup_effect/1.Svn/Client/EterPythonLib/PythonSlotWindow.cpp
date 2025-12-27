//Find in void CSlotWindow::ActivateSlot(DWORD dwIndex)
	if (!m_pSlotActiveEffect)
	{
		__CreateSlotEnableEffect();
	}

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	const int slot_index = MAX(0, pSlot->byyPlacedItemSize - 1);

	if (!m_pSlotActiveEffect[slot_index])
	{
		__CreateSlotEnableEffect(slot_index);
	}
#else
	if (!m_pSlotActiveEffect)
	{
		__CreateSlotEnableEffect();
	}
#endif

//Find in void CSlotWindow::ClearSlot(TSlot * pSlot)
	pSlot->dwCenterSlotNumber = 0xffffffff;

///Add
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	pSlot->d3Color = D3DXCOLOR(1.0f, 1.0f, 1.0f, 0.5f);
#endif

//Find in void CSlotWindow::OnUpdate()
	if (m_pSlotActiveEffect)
		m_pSlotActiveEffect->Update();

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	for (int i = 0; i < SLOT_ACTIVE_EFFECT_COUNT; i++)
	{
		if (m_pSlotActiveEffect[i])
			m_pSlotActiveEffect[i]->Update();
	}
#else
	if (m_pSlotActiveEffect)
		m_pSlotActiveEffect->Update();
#endif

//Find
		if (rSlot.bActive)
		if (m_pSlotActiveEffect)
		{
			int ix = m_rect.left + rSlot.ixPosition;
			int iy = m_rect.top + rSlot.iyPosition;
			m_pSlotActiveEffect->SetPosition(ix, iy);
			m_pSlotActiveEffect->Render();
		}

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
		if (rSlot.bActive)
		{
			const int slot_index = MAX(0, rSlot.byyPlacedItemSize - 1);
			if (m_pSlotActiveEffect[slot_index])
			{
				const int ix = m_rect.left + rSlot.ixPosition;
				const int iy = m_rect.top + rSlot.iyPosition;
				m_pSlotActiveEffect[slot_index]->SetPosition(ix, iy);
				m_pSlotActiveEffect[slot_index]->SetDiffuseColor(rSlot.d3Color.r, rSlot.d3Color.g, rSlot.d3Color.b, rSlot.d3Color.a);
				m_pSlotActiveEffect[slot_index]->Render();
			}
		}
#else
		if (rSlot.bActive)
		if (m_pSlotActiveEffect)
		{
			int ix = m_rect.left + rSlot.ixPosition;
			int iy = m_rect.top + rSlot.iyPosition;
			m_pSlotActiveEffect->SetPosition(ix, iy);
			m_pSlotActiveEffect->Render();
		}
#endif

//Find
void CSlotWindow::__CreateSlotEnableEffect()
{
	...
}

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
void CSlotWindow::__CreateSlotEnableEffect(int index)
{
	__DestroySlotEnableEffect(index);
	m_pSlotActiveEffect[index] = new CAniImageBox(NULL);

	/*char path[128];
	for (int i = 0; i <= 12; i++)
	{
		if (index == 0)
			snprintf(path, sizeof(path), "d:/ymir work/ui/public/slotactiveeffect/%02d.sub", i);
		else
			snprintf(path, sizeof(path), "d:/ymir work/ui/public/slotactiveeffect/slot%d/%02d.sub", (index + 1), i);

		m_pSlotActiveEffect[index]->AppendImage(path);
	}*/

	switch (index)
	{
	case 0:
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/00.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/01.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/02.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/03.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/04.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/05.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/06.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/07.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/08.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/09.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/10.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/11.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/12.sub");
		break;
	case 1:
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/00.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/01.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/02.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/03.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/04.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/05.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/06.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/07.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/08.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/09.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/10.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/11.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot2/12.sub");
		break;
	case 2:
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/00.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/01.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/02.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/03.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/04.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/05.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/06.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/07.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/08.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/09.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/10.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/11.sub");
		m_pSlotActiveEffect[index]->AppendImage("d:/ymir work/ui/public/slotactiveeffect/slot3/12.sub");
		break;
	}

	m_pSlotActiveEffect[index]->SetRenderingMode(CGraphicExpandedImageInstance::RENDERING_MODE_SCREEN);
	m_pSlotActiveEffect[index]->Show();
}
#else
void CSlotWindow::__CreateSlotEnableEffect()
{
	__DestroySlotEnableEffect();

	m_pSlotActiveEffect = new CAniImageBox(NULL);
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/00.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/01.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/02.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/03.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/04.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/05.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/06.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/07.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/08.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/09.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/10.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/11.sub");
	m_pSlotActiveEffect->AppendImage("d:/ymir work/ui/public/slotactiveeffect/12.sub");
	m_pSlotActiveEffect->SetRenderingMode(CGraphicExpandedImageInstance::RENDERING_MODE_SCREEN);
	m_pSlotActiveEffect->Show();
}
#endif

//Find
void CSlotWindow::__DestroySlotEnableEffect()
{
	...
}

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
void CSlotWindow::__DestroySlotEnableEffect(int index)
{
	if (m_pSlotActiveEffect[index])
	{
		delete m_pSlotActiveEffect[index];
		m_pSlotActiveEffect[index] = NULL;
	}
}
#else
void CSlotWindow::__DestroySlotEnableEffect()
{
	if (m_pSlotActiveEffect)
	{
		delete m_pSlotActiveEffect;
		m_pSlotActiveEffect = NULL;
	}
}
#endif

//Find in void CSlotWindow::__Initialize()
	m_pSlotActiveEffect = NULL;

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	for (int i = 0; i < SLOT_ACTIVE_EFFECT_COUNT; i++)
		m_pSlotActiveEffect[i] = NULL;
#else
	m_pSlotActiveEffect = NULL;
#endif

//Find in void CSlotWindow::Destroy()
	__DestroySlotEnableEffect();

///Change
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
	for (int i = 0; i < SLOT_ACTIVE_EFFECT_COUNT; i++)
		__DestroySlotEnableEffect(i);
#else
	__DestroySlotEnableEffect();
#endif

///Add new func
#if defined(__BL_ENABLE_PICKUP_ITEM_EFFECT__)
void CSlotWindow::SetSlotDiffuseColor(DWORD dwIndex, int iColorType)
{
	TSlot* pSlot;
	if (!GetSlotPointer(dwIndex, &pSlot))
		return;

	switch (iColorType)
	{
	case COLOR_TYPE_ORANGE:
		pSlot->d3Color = D3DXCOLOR(1.0f, 0.34509805f, 0.035294119f, 0.5f);
		break;
	case COLOR_TYPE_RED:
		pSlot->d3Color = D3DXCOLOR(1.0f, 0.0f, 0.0f, 0.5f);
		break;
	case COLOR_TYPE_GREEN:
		pSlot->d3Color = D3DXCOLOR(0.0f, 1.0f, 0.0f, 0.5f);
		break;
	case COLOR_TYPE_YELLOW:
		pSlot->d3Color = D3DXCOLOR(1.0f, 1.0f, 0.0f, 0.5f);
		break;
	case COLOR_TYPE_SKY:
		pSlot->d3Color = D3DXCOLOR(0.0f, 1.0f, 1.0f, 0.5f);
		break;
	case COLOR_TYPE_PINK:
		pSlot->d3Color = D3DXCOLOR(1.0f, 0.0f, 1.0f, 0.5f);
		break;
	case COLOR_TYPE_WHITE:
	default:
		pSlot->d3Color = D3DXCOLOR(1.0f, 1.0f, 1.0f, 0.5f);
		break;
	}
}
#endif