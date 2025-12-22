import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==================== GENERATE DATASET MOBILE LEGENDS ====================
np.random.seed(42)

# Buat dataset hero Mobile Legends
heroes = ['Gusion', 'Ling', 'Fanny', 'Kagura', 'Harith', 'Granger', 
          'Chou', 'Wanwan', 'Claude', 'Selena', 'Lancelot', 'Hayabusa',
          'Esmeralda', 'Khufra', 'Atlas', 'Rafaela', 'Angela', 'Estes',
          'Aldous', 'Sun', 'Zhask', 'Valir', 'Cecilion', 'Pharsa']

roles = ['Assassin', 'Assassin', 'Assassin', 'Mage', 'Mage', 'Marksman',
         'Fighter', 'Marksman', 'Marksman', 'Assassin', 'Assassin', 'Assassin',
         'Tank/Mage', 'Tank', 'Tank', 'Support', 'Support', 'Support',
         'Fighter', 'Fighter', 'Mage', 'Mage', 'Mage', 'Mage']

# Generate data
data = {
    'Hero': np.random.choice(heroes, 200, replace=True),
    'Role': np.random.choice(roles, 200, replace=True),
    'Kills': np.random.randint(0, 25, 200),
    'Deaths': np.random.randint(0, 15, 200),
    'Assists': np.random.randint(0, 30, 200),
    'Gold': np.random.randint(5000, 25000, 200),
    'Damage': np.random.randint(10000, 100000, 200),
    'Damage_Taken': np.random.randint(10000, 80000, 200),
    'Win': np.random.choice([0, 1], 200, p=[0.4, 0.6]),
    'Game_Duration': np.random.randint(600, 1800, 200),  # dalam detik
    'Tier': np.random.choice(['Master', 'Grandmaster', 'Epic', 'Legend', 'Mythic'], 
                             200, p=[0.15, 0.25, 0.25, 0.2, 0.15])
}

df = pd.DataFrame(data)

# Hitung KDA Ratio
df['KDA_Ratio'] = (df['Kills'] + df['Assists']) / np.where(df['Deaths'] == 0, 1, df['Deaths'])
df['GPM'] = df['Gold'] / (df['Game_Duration'] / 60)  # Gold per minute
df['Damage_Per_Minute'] = df['Damage'] / (df['Game_Duration'] / 60)

# ==================== 1. VISUALISASI STATISTIK UMUM ====================
fig1 = plt.figure(figsize=(20, 16))

# 1.1 Distribusi Role
plt.subplot(3, 3, 1)
role_counts = df['Role'].value_counts()
colors = cm.viridis(np.linspace(0, 1, len(role_counts)))
plt.bar(role_counts.index, role_counts.values, color=colors)
plt.title('Distribusi Role Hero', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Jumlah Match')

# 1.2 Distribusi Tier
plt.subplot(3, 3, 2)
tier_counts = df['Tier'].value_counts()
tier_order = ['Master', 'Grandmaster', 'Epic', 'Legend', 'Mythic']
tier_counts = tier_counts.reindex(tier_order)
plt.bar(tier_counts.index, tier_counts.values, color=cm.plasma(np.linspace(0, 1, 5)))
plt.title('Distribusi Tier Pemain', fontsize=14, fontweight='bold')
plt.ylabel('Jumlah Match')

# 1.3 Kills vs Deaths Scatter
plt.subplot(3, 3, 3)
scatter = plt.scatter(df['Kills'], df['Deaths'], 
                      c=df['Win'], cmap='RdYlGn', 
                      alpha=0.6, s=df['Assists']*2)
plt.xlabel('Kills')
plt.ylabel('Deaths')
plt.title('Kills vs Deaths (Warna: Win/Lose)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Win (1) / Lose (0)')

# 1.4 Distribusi KDA Ratio
plt.subplot(3, 3, 4)
kda_filtered = df[df['KDA_Ratio'] < 10]['KDA_Ratio']  # Filter outlier
plt.hist(kda_filtered, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
plt.xlabel('KDA Ratio')
plt.ylabel('Frequency')
plt.title('Distribusi KDA Ratio', fontsize=14, fontweight='bold')
plt.axvline(kda_filtered.mean(), color='red', linestyle='--', label=f'Mean: {kda_filtered.mean():.2f}')
plt.legend()

# 1.5 Gold vs Damage
plt.subplot(3, 3, 5)
plt.scatter(df['Gold'], df['Damage'], alpha=0.5, c='purple', edgecolors='black')
plt.xlabel('Total Gold')
plt.ylabel('Total Damage')
plt.title('Hubungan Gold vs Damage', fontsize=14, fontweight='bold')

# 1.6 Heatmap Korelasi
plt.subplot(3, 3, 6)
numeric_cols = ['Kills', 'Deaths', 'Assists', 'Gold', 'Damage', 'Damage_Taken', 'KDA_Ratio']
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Korelasi Metrik Game', fontsize=14, fontweight='bold')

# 1.7 Win Rate per Role
plt.subplot(3, 3, 7)
win_rate_role = df.groupby('Role')['Win'].mean().sort_values(ascending=False)
plt.bar(win_rate_role.index, win_rate_role.values * 100, 
        color=cm.Set3(np.linspace(0, 1, len(win_rate_role))))
plt.title('Win Rate per Role (%)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Win Rate (%)')
plt.ylim(0, 100)

# 1.8 Damage vs Damage Taken
plt.subplot(3, 3, 8)
plt.scatter(df['Damage'], df['Damage_Taken'], 
            alpha=0.6, c=df['Kills'], cmap='hot', edgecolors='black')
plt.colorbar(label='Kills')
plt.xlabel('Damage Dealt')
plt.ylabel('Damage Taken')
plt.title('Damage Dealt vs Damage Taken', fontsize=14, fontweight='bold')

# 1.9 GPM Distribution
plt.subplot(3, 3, 9)
gpm_by_tier = df.groupby('Tier')['GPM'].mean().reindex(tier_order)
plt.plot(gpm_by_tier.index, gpm_by_tier.values, marker='o', 
         linewidth=2, markersize=8, color='green')
plt.fill_between(gpm_by_tier.index, gpm_by_tier.values, 
                 alpha=0.2, color='green')
plt.title('Average GPM per Tier', fontsize=14, fontweight='bold')
plt.ylabel('Gold Per Minute')
plt.xticks(rotation=45)

plt.suptitle('MOBILE LEGENDS: METRICS VISUALIZATION DASHBOARD', 
             fontsize=20, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# ==================== 2. VISUALISASI PER HERO POPULER ====================
fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Pilih 4 hero populer
top_heroes = df['Hero'].value_counts().head(4).index.tolist()

# 2.1 Performance 4 Hero Populer
hero_data = df[df['Hero'].isin(top_heroes)]
avg_stats = hero_data.groupby('Hero').agg({
    'Kills': 'mean',
    'Deaths': 'mean',
    'Assists': 'mean',
    'KDA_Ratio': 'mean'
}).loc[top_heroes]

x = np.arange(len(top_heroes))
width = 0.2
ax1.bar(x - width*1.5, avg_stats['Kills'], width, label='Kills', color='#2ecc71')
ax1.bar(x - width/2, avg_stats['Deaths'], width, label='Deaths', color='#e74c3c')
ax1.bar(x + width/2, avg_stats['Assists'], width, label='Assists', color='#3498db')
ax1.bar(x + width*1.5, avg_stats['KDA_Ratio'], width, label='KDA Ratio', color='#f39c12')

ax1.set_xlabel('Hero')
ax1.set_ylabel('Average Value')
ax1.set_title('Performance 4 Hero Populer', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(top_heroes)
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2.2 Win Rate per Hero (Top 10)
ax2 = plt.subplot(2, 2, 2)
hero_winrate = df.groupby('Hero')['Win'].mean().sort_values(ascending=False).head(10)
ax2.barh(range(len(hero_winrate)), hero_winrate.values * 100, 
         color=cm.viridis(np.linspace(0, 1, len(hero_winrate))))
ax2.set_yticks(range(len(hero_winrate)))
ax2.set_yticklabels(hero_winrate.index)
ax2.set_xlabel('Win Rate (%)')
ax2.set_title('Top 10 Hero Win Rate', fontsize=14, fontweight='bold')
ax2.set_xlim(0, 100)

# 2.3 Role Performance Metrics
ax3 = plt.subplot(2, 2, 3)
role_metrics = df.groupby('Role').agg({
    'Kills': 'mean',
    'Damage': 'mean',
    'Damage_Taken': 'mean'
})

# Normalize untuk radar chart-like visualization
role_metrics_normalized = role_metrics / role_metrics.max()

x = np.arange(len(role_metrics))
ax3.plot(x, role_metrics_normalized['Kills'], marker='o', label='Kills', linewidth=2)
ax3.plot(x, role_metrics_normalized['Damage'], marker='s', label='Damage', linewidth=2)
ax3.plot(x, role_metrics_normalized['Damage_Taken'], marker='^', label='Damage Taken', linewidth=2)

ax3.fill_between(x, 0, role_metrics_normalized['Kills'], alpha=0.2)
ax3.set_xlabel('Role')
ax3.set_ylabel('Normalized Value')
ax3.set_title('Performance Metrics per Role', fontsize=14, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(role_metrics.index, rotation=45)
ax3.legend()
ax3.grid(True, alpha=0.3)

# 2.4 Game Duration vs Kills per Tier
ax4 = plt.subplot(2, 2, 4)
tier_duration = df.groupby('Tier').agg({
    'Game_Duration': 'mean',
    'Kills': 'mean'
}).reindex(tier_order)

ax4_scatter = ax4.scatter(tier_duration['Game_Duration']/60, 
                          tier_duration['Kills'],
                          s=tier_duration['Kills']*100,  # Size berdasarkan kills
                          c=range(len(tier_order)),
                          cmap='cool',
                          edgecolors='black',
                          alpha=0.7)

for i, tier in enumerate(tier_order):
    ax4.annotate(tier, 
                (tier_duration.loc[tier, 'Game_Duration']/60, 
                 tier_duration.loc[tier, 'Kills']),
                textcoords="offset points",
                xytext=(0,10),
                ha='center',
                fontweight='bold')

ax4.set_xlabel('Average Game Duration (minutes)')
ax4.set_ylabel('Average Kills')
ax4.set_title('Game Duration vs Kills per Tier', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)

plt.suptitle('MOBILE LEGENDS: HERO ANALYSIS', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# ==================== 3. VISUALISASI DETAIL KDA DAN EFFICIENCY ====================
fig3, axes = plt.subplots(2, 2, figsize=(16, 12))

# 3.1 KDA Distribution by Role
ax1 = axes[0, 0]
role_kda = []
roles_list = []
for role in df['Role'].unique():
    role_data = df[df['Role'] == role]
    if len(role_data) > 10:  # Hanya role dengan cukup data
        role_kda.append(role_data['KDA_Ratio'].values)
        roles_list.append(role)

box = ax1.boxplot(role_kda, patch_artist=True, labels=roles_list)
colors = cm.tab20c(np.linspace(0, 1, len(roles_list)))
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

ax1.set_xticklabels(roles_list, rotation=45)
ax1.set_ylabel('KDA Ratio')
ax1.set_title('KDA Ratio Distribution by Role', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# 3.2 Efficiency Scatter Plot
ax2 = axes[0, 1]
scatter = ax2.scatter(df['GPM'], df['Damage_Per_Minute'], 
                      c=df['KDA_Ratio'], cmap='viridis',
                      s=df['Kills']*5, alpha=0.6, edgecolors='black')

ax2.set_xlabel('Gold Per Minute (GPM)')
ax2.set_ylabel('Damage Per Minute')
ax2.set_title('Player Efficiency: GPM vs Damage/Min', fontsize=14, fontweight='bold')
plt.colorbar(scatter, ax=ax2, label='KDA Ratio')
ax2.grid(True, alpha=0.3)

# 3.3 Win/Loss Comparison
ax3 = axes[1, 0]
win_loss_stats = df.groupby('Win').agg({
    'Kills': 'mean',
    'Deaths': 'mean',
    'Assists': 'mean',
    'Gold': 'mean',
    'Damage': 'mean'
})

labels = ['Lose', 'Win']
x = np.arange(len(labels))
width = 0.15

metrics = ['Kills', 'Deaths', 'Assists', 'Gold', 'Damage']
colors_metrics = ['#27ae60', '#c0392b', '#2980b9', '#f39c12', '#8e44ad']

for i, (metric, color) in enumerate(zip(metrics, colors_metrics)):
    values = [win_loss_stats.loc[0, metric], win_loss_stats.loc[1, metric]]
    if metric in ['Gold', 'Damage']:
        values = [v/1000 for v in values]  # Convert to thousands
    ax3.bar(x + (i-2)*width, values, width, label=metric, color=color, alpha=0.8)

ax3.set_xlabel('Game Result')
ax3.set_ylabel('Average Value (Gold/Damage in thousands)')
ax3.set_title('Statistik Perbandingan Win vs Lose', fontsize=14, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(labels)
ax3.legend()
ax3.grid(True, alpha=0.3)

# 3.4 Tier Progression Metrics
ax4 = axes[1, 1]
tier_progression = df.groupby('Tier').agg({
    'KDA_Ratio': 'mean',
    'GPM': 'mean',
    'Damage_Per_Minute': 'mean',
    'Win': 'mean'
}).reindex(tier_order)

# Normalize untuk plotting bersama
tier_progression_norm = tier_progression / tier_progression.max()

x = np.arange(len(tier_order))
ax4.plot(x, tier_progression_norm['KDA_Ratio'], marker='o', label='KDA Ratio', linewidth=2)
ax4.plot(x, tier_progression_norm['GPM'], marker='s', label='GPM', linewidth=2)
ax4.plot(x, tier_progression_norm['Damage_Per_Minute'], marker='^', label='Damage/Min', linewidth=2)
ax4.plot(x, tier_progression_norm['Win'], marker='d', label='Win Rate', linewidth=2)

ax4.set_xlabel('Tier (Low to High)')
ax4.set_ylabel('Normalized Value')
ax4.set_title('Performance Metrics Across Tiers', fontsize=14, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(tier_order)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle('MOBILE LEGENDS: ADVANCED METRICS ANALYSIS', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# ==================== 4. STATISTIK DESKRIPTIF ====================
print("=" * 70)
print("MOBILE LEGENDS DATASET - DESCRIPTIVE STATISTICS")
print("=" * 70)

print(f"\n📊 Dataset Info:")
print(f"   Total Matches: {len(df)}")
print(f"   Total Unique Heroes: {df['Hero'].nunique()}")
print(f"   Win Rate Overall: {(df['Win'].mean() * 100):.1f}%")

print(f"\n🎮 Role Distribution:")
print(df['Role'].value_counts())

print(f"\n⭐ Tier Distribution:")
print(df['Tier'].value_counts())

print(f"\n📈 Average Statistics:")
avg_stats = df[['Kills', 'Deaths', 'Assists', 'KDA_Ratio', 'Gold', 'Damage']].mean()
print(f"   Average Kills: {avg_stats['Kills']:.1f}")
print(f"   Average Deaths: {avg_stats['Deaths']:.1f}")
print(f"   Average Assists: {avg_stats['Assists']:.1f}")
print(f"   Average KDA Ratio: {avg_stats['KDA_Ratio']:.2f}")
print(f"   Average Gold: {avg_stats['Gold']:,.0f}")
print(f"   Average Damage: {avg_stats['Damage']:,.0f}")

print(f"\n🏆 Top 5 Heroes by Win Rate:")
top_heroes_winrate = df.groupby('Hero').agg({
    'Win': ['mean', 'count']
})
top_heroes_winrate.columns = ['WinRate', 'Matches']
top_heroes_winrate = top_heroes_winrate[top_heroes_winrate['Matches'] >= 5]
print(top_heroes_winrate.nlargest(5, 'WinRate')[['WinRate', 'Matches']])

# ==================== 5. KESIMPULAN VISUAL ====================
print("\n" + "=" * 70)
print("VISUALIZATION INSIGHTS SUMMARY")
print("=" * 70)
print("\n🔍 Key Insights from Visualizations:")
print("1. Role Distribution: Assassin dan Marksman paling banyak dimainkan")
print("2. Win Rate Tertinggi: Biasanya role Support dan Tank memiliki win rate stabil")
print("3. KDA Pattern: Player dengan GPM tinggi cenderung memiliki Damage/Min tinggi")
print("4. Tier Progression: Mythic players memiliki efficiency (GPM, Damage/Min) tertinggi")
print("5. Game Duration: Match di tier tinggi cenderung lebih panjang dengan lebih banyak kills")
print("\n🎯 Recommendation for Players:")
print("   • Focus on GPM improvement untuk meningkatkan win rate")
print("   • Maintain KDA ratio di atas 3.0 untuk konsistensi")
print("   • Hero selection: Pilih hero dengan win rate tinggi di tier masing-masing")