#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Estrutura de configuração baseada no código do cliente
struct TConfig {
    int width;
    int height;
    int bpp;
    int frequency;
    int software_cursor;
    int object_culling;
    int visibility;
    float music_volume;
    float voice_volume;
    float gamma;
    int is_save_id;
    int save_id;
    int pre_loading_delay_time;
    int decompressed_texture;
    int windowed;
    int use_default_ime;
    int software_tiling;
    int shadow_level;
};

// Valores padrão
TConfig g_Config = {
    1366, 768, 32, 60, 0, 1, 3, 0.0f, 0.0f, 1.0f,
    0, 0, 20, 0, 1, 0, 0, 3
};

// Função para carregar configuração
bool LoadConfig(const char* filename) {
    FILE* fp = fopen(filename, "rt");
    if (!fp) return false;

    char buf[256];
    char command[256];
    char value[256];

    while (fgets(buf, sizeof(buf), fp)) {
        if (sscanf(buf, "%s %s", command, value) == 2) {
            if (strcmp(command, "WIDTH") == 0) g_Config.width = atoi(value);
            else if (strcmp(command, "HEIGHT") == 0) g_Config.height = atoi(value);
            else if (strcmp(command, "BPP") == 0) g_Config.bpp = atoi(value);
            else if (strcmp(command, "FREQUENCY") == 0) g_Config.frequency = atoi(value);
            else if (strcmp(command, "SOFTWARE_CURSOR") == 0) g_Config.software_cursor = atoi(value);
            else if (strcmp(command, "OBJECT_CULLING") == 0) g_Config.object_culling = atoi(value);
            else if (strcmp(command, "VISIBILITY") == 0) g_Config.visibility = atoi(value);
            else if (strcmp(command, "MUSIC_VOLUME") == 0) g_Config.music_volume = atof(value);
            else if (strcmp(command, "VOICE_VOLUME") == 0) g_Config.voice_volume = atof(value);
            else if (strcmp(command, "GAMMA") == 0) g_Config.gamma = atof(value);
            else if (strcmp(command, "IS_SAVE_ID") == 0) g_Config.is_save_id = atoi(value);
            else if (strcmp(command, "SAVE_ID") == 0) g_Config.save_id = atoi(value);
            else if (strcmp(command, "PRE_LOADING_DELAY_TIME") == 0) g_Config.pre_loading_delay_time = atoi(value);
            else if (strcmp(command, "DECOMPRESSED_TEXTURE") == 0) g_Config.decompressed_texture = atoi(value);
            else if (strcmp(command, "WINDOWED") == 0) g_Config.windowed = atoi(value);
            else if (strcmp(command, "USE_DEFAULT_IME") == 0) g_Config.use_default_ime = atoi(value);
            else if (strcmp(command, "SOFTWARE_TILING") == 0) g_Config.software_tiling = atoi(value);
            else if (strcmp(command, "SHADOW_LEVEL") == 0) g_Config.shadow_level = atoi(value);
        }
    }

    fclose(fp);
    return true;
}

// Função para salvar configuração
bool SaveConfig(const char* filename) {
    FILE* fp = fopen(filename, "wt");
    if (!fp) return false;

    fprintf(fp, "WIDTH\t\t\t\t%d\n", g_Config.width);
    fprintf(fp, "HEIGHT\t\t\t\t%d\n", g_Config.height);
    fprintf(fp, "BPP\t\t\t\t%d\n", g_Config.bpp);
    fprintf(fp, "FREQUENCY\t\t\t%d\n", g_Config.frequency);
    fprintf(fp, "SOFTWARE_CURSOR\t\t%d\n", g_Config.software_cursor);
    fprintf(fp, "OBJECT_CULLING\t\t\t%d\n", g_Config.object_culling);
    fprintf(fp, "VISIBILITY\t\t\t%d\n", g_Config.visibility);
    fprintf(fp, "MUSIC_VOLUME\t\t%.1f\n", g_Config.music_volume);
    fprintf(fp, "VOICE_VOLUME\t\t%.1f\n", g_Config.voice_volume);
    fprintf(fp, "GAMMA\t\t\t\t%.1f\n", g_Config.gamma);
    fprintf(fp, "IS_SAVE_ID\t\t\t%d\n", g_Config.is_save_id);
    fprintf(fp, "SAVE_ID\t\t\t%d\n", g_Config.save_id);
    fprintf(fp, "PRE_LOADING_DELAY_TIME\t%d\n", g_Config.pre_loading_delay_time);
    fprintf(fp, "DECOMPRESSED_TEXTURE\t%d\n", g_Config.decompressed_texture);
    fprintf(fp, "WINDOWED\t\t\t%d\n", g_Config.windowed);
    fprintf(fp, "USE_DEFAULT_IME\t\t%d\n", g_Config.use_default_ime);
    fprintf(fp, "SOFTWARE_TILING\t\t%d\n", g_Config.software_tiling);
    fprintf(fp, "SHADOW_LEVEL\t\t%d\n", g_Config.shadow_level);

    fclose(fp);
    return true;
}

// Função principal
int main() {
    // Tenta carregar configuração existente
    if (!LoadConfig("config/metin2.cfg") && !LoadConfig("metin2.cfg")) {
        printf("Nenhuma configuracao encontrada, usando valores padrao.\n");
    }

    // Aqui seria implementada a interface gráfica
    // Por enquanto, vamos salvar com valores padrão
    printf("Metin2 Configuration Tool\n");
    printf("========================\n\n");

    printf("Configuracao atual:\n");
    printf("Resolucao: %dx%d\n", g_Config.width, g_Config.height);
    printf("Modo: %s\n", g_Config.windowed ? "Janela" : "Tela Cheia");
    printf("BPP: %d\n", g_Config.bpp);
    printf("\n");

    // Salva a configuração
    if (SaveConfig("config/metin2.cfg")) {
        printf("✓ Configuracao salva com sucesso em config/metin2.cfg\n");
    } else {
        printf("✗ Erro ao salvar configuracao!\n");
        return 1;
    }

    printf("\nPressione qualquer tecla para continuar...");
    getchar();

    return 0;
}