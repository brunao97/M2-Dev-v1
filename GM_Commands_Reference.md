# Comandos GM - Metin2 Server

## Níveis de Autoridade GM

| Nível | Valor | Descrição |
|-------|-------|-----------|
| GM_PLAYER | 0 | Jogador normal |
| GM_LOW_WIZARD | 1 | GM Básico |
| GM_WIZARD | 2 | GM Intermediário |
| GM_HIGH_WIZARD | 3 | GM Avançado |
| GM_GOD | 4 | GM Mestre |
| GM_IMPLEMENTOR | 5 | Administrador/Implementador |

## Comandos por Nível de Autoridade

### GM_PLAYER (0) - Comandos para Jogadores Normais
- `who` - Lista jogadores online
- `war` - Declara guerra entre guildas
- `nowar` - Cancela guerra entre guildas
- `stat` - Mostra estatísticas do personagem
- `stat-` - Remove pontos de status
- `stat_reset` - Reseta pontos de status
- `restart_here` - Reinicia no local atual
- `restart_town` - Reinicia na cidade
- `quit` - Sai do jogo
- `skillup` - Aumenta nível de skill
- `gskillup` - Aumenta skill de guilda
- `pvp` - Ativa/desativa modo PvP
- `safebox_close` - Fecha baú seguro
- `safebox_password` - Define senha do baú
- `mall_password` - Define senha do mall
- `mall_close` - Fecha mall
- `ungroup` - Sai do grupo
- `pkmode` - Ativa/desativa modo PK
- `messenger_auth` - Autorização de mensageiro
- `set_walk_mode` - Define modo caminhada
- `set_run_mode` - Define modo corrida
- `setblockmode` - Define modo bloqueio
- `unmount` - Desmonta cavalo/montaria
- `view_equip` - Visualiza equipamento
- `block_chat` - Bloqueia chat
- `block_chat_list` - Lista bloqueios de chat
- `vote_block_chat` - Vota para bloquear chat
- `emotion_allow` - Permite emoções
- `kiss` - Beijo
- `slap` - Tapa
- `french_kiss` - Beijo francês
- `clap` - Aplausos
- `cheer1` - Torcida 1
- `cheer2` - Torcida 2
- `dance1` - Dança 1
- `dance2` - Dança 2
- `dance3` - Dança 3
- `dance4` - Dança 4
- `dance5` - Dança 5
- `dance6` - Dança 6
- `congratulation` - Parabéns
- `forgive` - Perdão
- `angry` - Raiva
- `attractive` - Atraente
- `sad` - Triste
- `shy` - Tímido
- `cheerup` - Anime-se
- `banter` - Provocação
- `joy` - Alegria
- `user_horse_ride` - Monta cavalo
- `user_horse_back` - Volta para cavalo
- `user_horse_feed` - Alimenta cavalo
- `hair` - Muda cabelo
- `cube` - Sistema de cubo
- `gift` - Sistema de presentes
- `in_game_mall` - Mall do jogo
- `dice` - Joga dados
- `주사위` - Joga dados (coreano)
- `click_mall` - Mall por clique
- `ride` - Sistema de montaria
- `costume` - Sistema de fantasias
- `dragon_soul` - Almas de dragão
- `ds_list` - Lista almas de dragão

### GM_LOW_WIZARD (1) - Comandos GM Básicos
- `warp` - Teleporta para coordenadas
- `notice_map` - Notícia no mapa
- `level` - Define nível do personagem
- `geteventflag` - Obtém flag de evento
- `state` - Mostra estado do personagem
- `stun` - Atordoa alvo
- `slow` - Enlentece alvo
- `respawn` - Respawna personagem
- `invisible` - Torna invisível
- `setskill` - Define skill
- `gwlist` - Lista guerras de guilda
- `gwstop` - Para guerra de guilda
- `gwcancel` - Cancela guerra de guilda
- `gstate` - Estado da guilda
- `getqf` - Obtém quest flag
- `setqf` - Define quest flag
- `delqf` - Remove quest flag
- `set_state` - Define estado
- `detaillog` - Log detalhado
- `monsterlog` - Log de monstros
- `forgetme` - Faz monstros esquecerem
- `aggregate` - Agrega monstros
- `attract_ranger` - Atrai arqueiros
- `pull_monster` - Puxa monstros
- `polymorph` - Polimorfismo
- `affect_remove` - Remove efeitos
- `horse_state` - Estado do cavalo
- `horse_level` - Nível do cavalo
- `horse_ride` - Monta cavalo
- `horse_summon` - Invoca cavalo
- `horse_unsummon` - Desinvoca cavalo
- `horse_set_stat` - Define stats do cavalo
- `show_arena_list` - Mostra lista arena
- `end_all_duel` - Termina todos duelos
- `end_duel` - Termina duelo
- `duel` - Inicia duelo
- `con+` - Aumenta constituição
- `int+` - Aumenta inteligência
- `str+` - Aumenta força
- `dex+` - Aumenta destreza
- `break_marriage` - Quebra casamento
- `show_quiz` - Mostra quiz
- `log_oxevent` - Log evento ox
- `get_oxevent_att` - Obtém participantes ox
- `effect` - Aplica efeito
- `threeway_info` - Info guerra tripla
- `threeway_myinfo` - Minha info guerra tripla
- `mto` - Teleporta monarca
- `mtr` - Transferência monarca
- `minfo` - Info monarca
- `mtax` - Taxa monarca
- `mmob` - Mob monarca
- `rmcandidacy` - Remove candidatura
- `inventory` - Mostra inventário
- `siege` - Sistema de cerco
- `mnotice` - Notícia monarca
- `weeklyevent` - Evento semanal
- `get_mob_count` - Conta mobs
- `item_id_list` - Lista IDs de itens
- `set_socket` - Define socket
- `tcon` - Define constituição
- `tint` - Define inteligência
- `tstr` - Define força
- `tdex` - Define destreza
- `cannot_dead` - Imortalidade
- `can_dead` - Remove imortalidade
- `full_set` - Full set
- `item_full_set` - Full set itens
- `attr_full_set` - Full set atributos
- `all_skill_master` - Todas skills master
- `use_item` - Usa item
- `do_clear_affect` - Limpa efeitos

### GM_WIZARD (2) - Comandos GM Intermediários
- `purge` - Remove todos os mobs/itens
- `weaken` - Enfraquece alvo
- `respawn` - Respawna personagem

### GM_HIGH_WIZARD (3) - Comandos GM Avançados
- `user` - Mostra informações do usuário
- `notice` - Notícia global
- `big_notice` - Notícia grande
- `monarch_notice` - Notícia monarca
- `eventflag` - Define flag de evento
- `mob` - Invoca monstro
- `mob_ld` - Invoca monstro com direção
- `ma` - Mob agressivo
- `mc` - Mob covarde
- `mm` - Mob por mapa
- `kill` - Mata alvo
- `ipurge` - Remove itens
- `group` - Grupo de mobs
- `grrandom` - Grupo aleatório
- `reset` - Reseta personagem
- `greset` - Reseta guilda
- `advance` - Avança nível
- `makeguild` - Cria guilda
- `deleteguild` - Remove guilda
- `safebox_size` - Define tamanho baú
- `priv_empire` - Privilégio império
- `priv_guild` - Privilégio guilda
- `polyitem` - Polimorfismo item
- `socketitem` - Item com socket
- `xmas_boom` - Efeito natal boom
- `xmas_snow` - Efeito natal neve
- `xmas_santa` - Efeito natal papai noel
- `jy` - Bloqueia chat (?)
- `clear_land` - Limpa terreno
- `frog` - Transforma em sapo
- `eclipse` - Eclipse
- `eventhelper` - Ajudante de eventos

### GM_GOD (4) - Comandos GM Mestres
- `item` - Cria item
- `weaken` - Enfraquece alvo

### GM_IMPLEMENTOR (5) - Comandos Administradores
- `set` - Define propriedades avançadas
- `book` - Sistema de livros
- `refine_rod` - Refinar vara
- `refine_pick` - Refinar picareta
- `max_pick` - Max picareta
- `fish_simul` - Simulação pesca
- `qf` - Quest flag
- `clear_quest` - Limpa quests
- `setjob` - Define job/skill group
- `setskillother` - Define skill em outro
- `setskillpoint` - Define pontos de skill
- `reload` - Recarrega configurações
- `cooltime` - Define cooldown
- `console` - Console
- `shutdow` - Desliga servidor
- `shutdown` - Desliga servidor
- `private` - Modo privado
- `observer` - Modo observador
- `saveati` - Salva atributos para imagem
- `change_attr` - Muda atributo
- `add_attr` - Adiciona atributo
- `add_socket` - Adiciona socket
- `temp` - Comando temporário
- `check_mmoney` - Checa dinheiro monarca
- `flush` - Flush sistema
- `special_item` - Item especial

## Comandos Especiais e Transferência
- `transfer` - Transfere personagem
- `goto` - Vai para localização
- `dc` - Desconecta jogador

## Comandos de Monarca
- `elect` - Eleição monarca
- `setmonarch` - Define monarca
- `rmmonarch` - Remove monarca

## Sistema de Construção
- `build` - Construir

## Sistema de Emoções e Interações
Todos os comandos de emoção estão disponíveis para GM_PLAYER e acima.

## Sistema de Cavalo/Montaria
- `horse_state` - Estado
- `horse_level` - Nível
- `horse_ride` - Montar
- `horse_summon` - Invocar
- `horse_unsummon` - Desinvocar
- `horse_set_stat` - Definir stats

## Sistema de Batalha e Duelo
- `show_arena_list` - Lista arena
- `end_all_duel` - Terminar todos duelos
- `end_duel` - Terminar duelo específico
- `duel` - Iniciar duelo

## Sistema de Atributos e Stats
- `full_set` - Conjunto completo
- `item_full_set` - Itens completos
- `attr_full_set` - Atributos completos
- `all_skill_master` - Todas skills master

## Sistema de Eventos
- `eventflag` - Flags de evento
- `geteventflag` - Obter flag evento
- `xmas_*` - Eventos natalinos
- `weeklyevent` - Evento semanal
- `oxevent` - Evento OX

## Sistema de Logs e Monitoramento
- `detaillog` - Log detalhado
- `monsterlog` - Log monstros
- `로그를보여줘` - Mostrar logs (coreano)

## Sistema de Guildas e Guerras
- `gwlist` - Lista guerras guilda
- `gwstop` - Parar guerra guilda
- `gwcancel` - Cancelar guerra guilda
- `gstate` - Estado guilda

## Sistema de Chat e Comunicação
- `notice` - Notícia global
- `notice_map` - Notícia mapa
- `big_notice` - Notícia grande
- `monarch_notice` - Notícia monarca
- `block_chat` - Bloquear chat

## Sistema de Quests
- `qf` - Quest flag
- `getqf` - Obter quest flag
- `setqf` - Definir quest flag
- `delqf` - Remover quest flag
- `clear_quest` - Limpar quests

## Sistema de Items e Equipamentos
- `item` - Criar item
- `ipurge` - Remover itens
- `socketitem` - Item com socket
- `add_socket` - Adicionar socket
- `change_attr` - Mudar atributo
- `add_attr` - Adicionar atributo

## Sistema de Monstros e NPCs
- `mob` - Invocar monstro
- `mob_ld` - Monstro com localização/direção
- `ma` - Monstro agressivo
- `mc` - Monstro covarde
- `mm` - Monstro por mapa
- `purge` - Remover todos
- `get_mob_count` - Contar monstros

## Sistema de Polimorfismo e Transformações
- `polymorph` - Polimorfismo
- `polyitem` - Item polimórfico
- `frog` - Transformar em sapo

## Sistema de Privacidade e Moderação
- `private` - Modo privado
- `observer` - Modo observador
- `invisible` - Invisibilidade
- `priv_empire` - Privilégio império
- `priv_guild` - Privilégio guilda

## Comandos de Debug e Desenvolvimento
- `reload` - Recarregar configurações
- `console` - Console
- `flush` - Flush sistema
- `temp` - Comando temporário
- `saveati` - Salvar atributos
- `special_item` - Item especial

---

*Este documento foi gerado automaticamente a partir do código fonte do servidor Metin2.*