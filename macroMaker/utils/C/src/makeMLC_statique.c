// # ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° °
// #
// #            Implemented at CRCT - INSERM (UMR1037) Team 15
// #            Toulouse - France - 2016
// #            tony.younes@inserm.fr & fredric.chatrie@inserm.fr
// #
// #            This file is NOT an open source. Contains confidential
// #            information from Varian Medical Systems (Palo Alto, CA)
// #
// # ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° ° °


#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char **argv)
{
    FILE *pf;
    FILE *pf2;
    FILE *pf3;
    FILE *pf4;
    FILE *pf5;
    FILE *pf6;
    FILE *pf7;
    FILE *pf8;



    // gantry rot
    double D,m,X1,Y1,J,inputValue,XQLT_SUP,XQLI_SUP,XQLT_INF,XQLI_INF,XHLT_SUP,XHLI_SUP;
    double XHLT_INF,XHLI_INF,Yinf,Zinf,alpha1,alpha2,YHLT_SUP,YHLI_SUP,YHLT_INF,YHLI_INF;
    double ZHLT_SUP,ZHLI_SUP,ZHLT_INF,ZHLI_INF,YQLT_SUP,YQLI_SUP,YQLT_INF,YQLI_INF;
    double ZQLT_SUP,ZQLI_SUP,ZQLT_INF,ZQLI_INF,N,D1,DEC,m2,D2;
    double InterHL,InterQL;
    int failure,n,iii;
    char myChar;


    double position[16]={0},pasHLIHLT,pasHLIQLT,pasQLTQLI,pasQLIHLT;
    double min,max,pas;
    int nbLamesTotal,nbLamesH,nbLamesQ,i;
    double *ech,*pos;
    //min=-10;
    min=-9.0;
    max=-min;
    //pas=0.5;
	pas=0.45;


    InterHL=0.131;//0.135 is the smallest value where no overlap corresponding to interleaf distance is found
    InterQL=0.036;//0.036 is the smallest value where no overlap corresponding to interleaf distance is found
   // pasHLIHLT=2.542+0.125;
    pasHLIHLT=2.542+InterHL;
    pasHLIQLT=1.907+0.036;
   // pasQLTQLI=1.267+0.025;
   pasQLTQLI=1.267+InterQL;
    pasQLIHLT=1.902+0.036;


    nbLamesTotal=58;
    nbLamesH=13;
    nbLamesQ=nbLamesTotal-2*nbLamesH;
    J=-90.0;
    D=100.27;
    D1=51.975;
    D2=51.975;
    m=D1/D;
    m2=D2/D;
    XHLT_SUP=17.6;
    XHLI_SUP=16.25;
    XHLT_INF=-15.9;
    XHLI_INF=-17.25;

    XQLT_SUP=17.61;
    XQLI_SUP=16.535;

    XQLT_INF=-16.14;
    XQLI_INF=-17.215;

    int main(int argc, char *argv[]);
    FILE *f;
    //58 lames en mouvement; les outboard leaf ne sont pas considérés dans ce cas, sinon mettre 60


    char ccc[120];
    char cc[120];
    char c[120];

    double x[120];
    int b;
    //f = fopen ("MLC_A_Leaves.txt" ,"r");
    //f = fopen ("dec_mlc5jaw7.mlc" ,"r");
    f = fopen(argv[1], "r");
   // for (i=0;i<58;i++)

  for(iii=0;iii<14;iii++)
	{
	while(myChar!='\n')
	{
	fscanf(f,"%c",&myChar);
	//printf("%c ",myChar);
	}
	myChar=1;
	}

	//printf("ok1\n");

 for (i=0;i<120;i++)
  	{
        	fscanf(f,"%s\n %s %s %lf\n",c,cc,ccc,&x[i]);
        	//printf ("X%d %.20lf\n",i,x[i]);
    }
    fclose(f);





    ech=(double*)malloc(nbLamesTotal*sizeof(double));
    pos=(double*)malloc(nbLamesTotal*sizeof(double));



        pf =fopen("QLT_SUP.dat","w");
        pf2 =fopen("QLI_SUP.dat","w");
        pf3 =fopen("QLT_INF.dat","w");
        pf4 =fopen("QLI_INF.dat","w");
        pf5 =fopen("HLT_SUP.dat","w");
        pf6 =fopen("HLI_SUP.dat","w");
        pf7 =fopen("HLT_INF.dat","w");
        pf8 =fopen("HLI_INF.dat","w");


        fprintf(pf,"0 ");
        fprintf(pf2,"0 ");
        fprintf(pf3,"0 ");
        fprintf(pf4,"0 ");
        fprintf(pf5,"0 ");
        fprintf(pf6,"0 ");
        fprintf(pf7,"0 ");
        fprintf(pf8,"0 ");

        //DEC=0.2542;
        //DEC=0.6530095;
        DEC=0.6530095;
        ech[0]=min; 		//ech[0]=-4
        ech[1]=min+pas;    //ech[1]=-4+0.25=-3.75
        pos[0]=-53.3745-DEC-InterHL;
        //pos[1]=-50.7075;
        pos[1]=-50.8325-DEC;




        fprintf(pf5,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[1]/D),J+10*m*x[2],XHLT_SUP*cos(atan(ech[1]/D)),pos[1]+sqrt((XHLT_SUP*XHLT_SUP)-((XHLT_SUP*cos(atan(ech[1]/D)))*(XHLT_SUP*cos(atan(ech[1]/D))))));
        fprintf(pf6,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[0]/D),J+10*m*x[1],XHLI_SUP*cos(atan(ech[0]/D)),pos[0]+sqrt((XHLI_SUP*XHLI_SUP)-((XHLI_SUP*cos(atan(ech[0]/D)))*(XHLI_SUP*cos(atan(ech[0]/D))))));
        fprintf(pf7,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[1]/D),J+10*m*x[2],XHLT_INF*cos(atan(ech[1]/D)),pos[1]-sqrt((XHLT_INF*XHLT_INF)-((XHLT_INF*cos(atan(ech[1]/D)))*(XHLT_INF*cos(atan(ech[1]/D))))));
        fprintf(pf8,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[0]/D),J+10*m*x[1],XHLI_INF*cos(atan(ech[0]/D)),pos[0]-sqrt((XHLI_INF*XHLI_INF)-((XHLI_INF*cos(atan(ech[0]/D)))*(XHLI_INF*cos(atan(ech[0]/D))))));


        for (i=2; i<nbLamesTotal; i+=2)
        	{
            //printf("\n BONS !!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
            if(i<nbLamesH-1 || i>nbLamesTotal-nbLamesH)
            	{
                ech[i]=ech[i-1]+pas;
                ech[i+1]=ech[i]+pas;


            	}
            else
            {

                if(i==nbLamesH-1){
                    ech[i]=ech[i-1]+pas;
                    ech[i+1]=ech[i]+pas/2;
                }
                else if(i==(nbLamesTotal/2-1)){
                    ech[i]=ech[i-1]+pas/2;
                    ech[i+1]=ech[i];
                }
                else{
                    ech[i]=ech[i-1]+pas/2;
                    ech[i+1]=ech[i]+pas/2;
                }
            }

            alpha1=atan(ech[i]/D);
            alpha2=atan(ech[i+1]/D);


            YQLT_SUP=XQLT_SUP*cos(alpha2);
            YQLI_SUP=XQLI_SUP*cos(alpha1);

            YQLT_INF=XQLT_INF*cos(alpha2);
            YQLI_INF=XQLI_INF*cos(alpha1);

            YHLT_SUP=XHLT_SUP*cos(alpha2);
            YHLI_SUP=XHLI_SUP*cos(alpha1);

            YHLT_INF=XHLT_INF*cos(alpha2);
            YHLI_INF=XHLI_INF*cos(alpha1);



            if(i<(nbLamesTotal/2)){

                ZQLT_SUP=sqrt((XQLT_SUP*XQLT_SUP)-(YQLT_SUP*YQLT_SUP));
                ZQLI_SUP=sqrt((XQLI_SUP*XQLI_SUP)-(YQLI_SUP*YQLI_SUP));

                ZQLT_INF=sqrt((XQLT_INF*XQLT_INF)-(YQLT_INF*YQLT_INF));
                ZQLI_INF=sqrt((XQLI_INF*XQLI_INF)-(YQLI_INF*YQLI_INF));

                ZHLT_SUP=sqrt((XHLT_SUP*XHLT_SUP)-(YHLT_SUP*YHLT_SUP));
                ZHLI_SUP=sqrt((XHLI_SUP*XHLI_SUP)-(YHLI_SUP*YHLI_SUP));

                ZHLT_INF=sqrt((XHLT_INF*XHLT_INF)-(YHLT_INF*YHLT_INF));
                ZHLI_INF=sqrt((XHLI_INF*XHLI_INF)-(YHLI_INF*YHLI_INF));
            }
            else{

                ZQLT_SUP=-sqrt((XQLT_SUP*XQLT_SUP)-(YQLT_SUP*YQLT_SUP));
                ZQLI_SUP=-sqrt((XQLI_SUP*XQLI_SUP)-(YQLI_SUP*YQLI_SUP));

                ZQLT_INF=-sqrt((XQLT_INF*XQLT_INF)-(YQLT_INF*YQLT_INF));
                ZQLI_INF=-sqrt((XQLI_INF*XQLI_INF)-(YQLI_INF*YQLI_INF));

                ZHLT_SUP=-sqrt((XHLT_SUP*XHLT_SUP)-(YHLT_SUP*YHLT_SUP));
                ZHLI_SUP=-sqrt((XHLI_SUP*XHLI_SUP)-(YHLI_SUP*YHLI_SUP));

                ZHLT_INF=-sqrt((XHLT_INF*XHLT_INF)-(YHLT_INF*YHLT_INF));
                ZHLI_INF=-sqrt((XHLI_INF*XHLI_INF)-(YHLI_INF*YHLI_INF));
            }




            if(i<nbLamesH-1 || i>nbLamesTotal-nbLamesH-1){


                pos[i]=pos[i-1]+pasHLIHLT;
                pos[i+1]=pos[i]+pasHLIHLT;



                fprintf(pf5,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m*x[i+2],YHLT_SUP,pos[i+1]+ZHLT_SUP); //pos+Zsup1
                fprintf(pf6,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m*x[i+1],YHLI_SUP,pos[i]+ZHLI_SUP); //pos-Zsup2
                fprintf(pf7,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m*x[i+2],YHLT_INF,pos[i+1]-ZHLT_INF); //pos+ZHLT_INF
                fprintf(pf8,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m*x[i+1],YHLI_INF,pos[i]-ZHLI_INF); //pos-Zsup2

            }
            else{


                if(i==nbLamesH-1){
                    //printf("\n PB ICI !!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
                    pos[i]=pos[i-1]+pasHLIHLT;
                    pos[i+1]=pos[i]+pasHLIQLT;

                    fprintf(pf6,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m*x[i+1],YHLI_SUP,pos[i]+ZHLI_SUP); //pos-Zsup2
                    fprintf(pf8,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m*x[i+1],YHLI_INF,pos[i]-ZHLI_INF); //pos-Zsup2
                    fprintf(pf,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m*x[i+2],YQLT_SUP,pos[i+1]+ZQLT_SUP); //pos+Zsup1
                    fprintf(pf3,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m*x[i+2],YQLT_INF,pos[i+1]-ZQLT_INF); //pos+ZQLT_INF
                }
                else if(i==nbLamesTotal-nbLamesH-1){
                    pos[i]=pos[i-1]+pasQLTQLI;
                    pos[i+1]=pos[i]+pasQLIHLT;
                    fprintf(pf5,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m*x[i+2],YHLT_SUP,pos[i+1]+ZHLT_SUP); //pos+Zsup1
                    fprintf(pf7,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m*x[i+2],YHLT_INF,pos[i+1]-ZHLT_INF); //pos+ZHLT_INF
                    fprintf(pf2,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m2*x[i+1],YQLI_SUP,pos[i]+ZQLI_SUP); //pos-Zsup2
                    fprintf(pf4,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m2*x[i+1],YQLI_INF,pos[i]-ZQLI_INF); //pos-Zsup2

                }
                else{
                    pos[i]=pos[i-1]+pasQLTQLI;
                    pos[i+1]=pos[i]+pasQLTQLI;

                    fprintf(pf,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m2*x[i+2],YQLT_SUP,pos[i+1]+ZQLT_SUP); //pos+Zsup1
                    fprintf(pf2,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m2*x[i+1],YQLI_SUP,pos[i]+ZQLI_SUP); //pos-Zsup2
                    fprintf(pf3,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J+10*m2*x[i+2],YQLT_INF,pos[i+1]-ZQLT_INF); //pos+ZQLT_INF
                    fprintf(pf4,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J+10*m2*x[i+1],YQLI_INF,pos[i]-ZQLI_INF); //pos-Zsup2

                }
            }

        }




        //printf("\ncompute valuesMLC.dat for first Bank...ok\n");
        fclose(pf);
        fclose(pf2);
        fclose(pf3);
        fclose(pf4);
        fclose(pf5);
        fclose(pf6);
        fclose(pf7);
        fclose(pf8);


        /* SECOND BANK 180 */

        pf =fopen("QLT_SUP180.dat","w");
        pf2 =fopen("QLI_SUP180.dat","w");
        pf3 =fopen("QLT_INF180.dat","w");
        pf4 =fopen("QLI_INF180.dat","w");
        pf5 =fopen("HLT_SUP180.dat","w");
        pf6 =fopen("HLI_SUP180.dat","w");
        pf7 =fopen("HLT_INF180.dat","w");
        pf8 =fopen("HLI_INF180.dat","w");

        fprintf(pf,"0 ");
        fprintf(pf2,"0 ");
        fprintf(pf3,"0 ");
        fprintf(pf4,"0 ");
        fprintf(pf5,"0 ");
        fprintf(pf6,"0 ");
        fprintf(pf7,"0 ");
        fprintf(pf8,"0 ");




        ech[0]=min; 		//ech[0]=-4
        ech[1]=min+pas;    //ech[1]=-4+0.25=-3.75
        pos[0]=-53.3745-DEC-InterHL;
        //pos[1]=-50.7075;
        pos[1]=-50.8325-DEC;





        fprintf(pf5,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[1]/D),J-10*m*x[62],XHLT_SUP*cos(atan(ech[1]/D)),pos[1]+sqrt((XHLT_SUP*XHLT_SUP)-((XHLT_SUP*cos(atan(ech[1]/D)))*(XHLT_SUP*cos(atan(ech[1]/D))))));
        fprintf(pf6,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[0]/D),J-10*m*x[61],XHLI_SUP*cos(atan(ech[0]/D)),pos[0]+sqrt((XHLI_SUP*XHLI_SUP)-((XHLI_SUP*cos(atan(ech[0]/D)))*(XHLI_SUP*cos(atan(ech[0]/D))))));
        fprintf(pf7,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[1]/D),J-10*m*x[62],XHLT_INF*cos(atan(ech[1]/D)),pos[1]-sqrt((XHLT_INF*XHLT_INF)-((XHLT_INF*cos(atan(ech[1]/D)))*(XHLT_INF*cos(atan(ech[1]/D))))));
        fprintf(pf8,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",atan(ech[0]/D),J-10*m*x[61],XHLI_INF*cos(atan(ech[0]/D)),pos[0]-sqrt((XHLI_INF*XHLI_INF)-((XHLI_INF*cos(atan(ech[0]/D)))*(XHLI_INF*cos(atan(ech[0]/D))))));


        for (i=2; i<nbLamesTotal; i+=2){
            if(i<nbLamesH-1 || i>nbLamesTotal-nbLamesH){
                ech[i]=ech[i-1]+pas;
                ech[i+1]=ech[i]+pas;


            }
            else{

                if(i==nbLamesH-1){
                    ech[i]=ech[i-1]+pas;
                    ech[i+1]=ech[i]+pas/2;
                }
                else if(i==(nbLamesTotal/2-1)){
                    ech[i]=ech[i-1]+pas/2;
                    ech[i+1]=ech[i];
                }
                else{
                    ech[i]=ech[i-1]+pas/2;
                    ech[i+1]=ech[i]+pas/2;
                }
            }

            alpha1=atan(ech[i]/D);
            alpha2=atan(ech[i+1]/D);


            YQLT_SUP=XQLT_SUP*cos(alpha2);
            YQLI_SUP=XQLI_SUP*cos(alpha1);

            YQLT_INF=XQLT_INF*cos(alpha2);
            YQLI_INF=XQLI_INF*cos(alpha1);

            YHLT_SUP=XHLT_SUP*cos(alpha2);
            YHLI_SUP=XHLI_SUP*cos(alpha1);

            YHLT_INF=XHLT_INF*cos(alpha2);
            YHLI_INF=XHLI_INF*cos(alpha1);



            if(i<(nbLamesTotal/2)){

                ZQLT_SUP=sqrt((XQLT_SUP*XQLT_SUP)-(YQLT_SUP*YQLT_SUP));
                ZQLI_SUP=sqrt((XQLI_SUP*XQLI_SUP)-(YQLI_SUP*YQLI_SUP));

                ZQLT_INF=sqrt((XQLT_INF*XQLT_INF)-(YQLT_INF*YQLT_INF));
                ZQLI_INF=sqrt((XQLI_INF*XQLI_INF)-(YQLI_INF*YQLI_INF));

                ZHLT_SUP=sqrt((XHLT_SUP*XHLT_SUP)-(YHLT_SUP*YHLT_SUP));
                ZHLI_SUP=sqrt((XHLI_SUP*XHLI_SUP)-(YHLI_SUP*YHLI_SUP));

                ZHLT_INF=sqrt((XHLT_INF*XHLT_INF)-(YHLT_INF*YHLT_INF));
                ZHLI_INF=sqrt((XHLI_INF*XHLI_INF)-(YHLI_INF*YHLI_INF));
            }
            else{

                ZQLT_SUP=-sqrt((XQLT_SUP*XQLT_SUP)-(YQLT_SUP*YQLT_SUP));
                ZQLI_SUP=-sqrt((XQLI_SUP*XQLI_SUP)-(YQLI_SUP*YQLI_SUP));

                ZQLT_INF=-sqrt((XQLT_INF*XQLT_INF)-(YQLT_INF*YQLT_INF));
                ZQLI_INF=-sqrt((XQLI_INF*XQLI_INF)-(YQLI_INF*YQLI_INF));

                ZHLT_SUP=-sqrt((XHLT_SUP*XHLT_SUP)-(YHLT_SUP*YHLT_SUP));
                ZHLI_SUP=-sqrt((XHLI_SUP*XHLI_SUP)-(YHLI_SUP*YHLI_SUP));

                ZHLT_INF=-sqrt((XHLT_INF*XHLT_INF)-(YHLT_INF*YHLT_INF));
                ZHLI_INF=-sqrt((XHLI_INF*XHLI_INF)-(YHLI_INF*YHLI_INF));
            }


            if(i<nbLamesH-1 || i>nbLamesTotal-nbLamesH-1){


                pos[i]=pos[i-1]+pasHLIHLT;
                pos[i+1]=pos[i]+pasHLIHLT;

                fprintf(pf5,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m*x[i+62],YHLT_SUP,pos[i+1]+ZHLT_SUP); //pos+Zsup1
                fprintf(pf6,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m*x[i+61],YHLI_SUP,pos[i]+ZHLI_SUP); //pos-Zsup2
                fprintf(pf7,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m*x[i+62],YHLT_INF,pos[i+1]-ZHLT_INF); //pos+ZHLT_INF
                fprintf(pf8,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m*x[i+61],YHLI_INF,pos[i]-ZHLI_INF); //pos-Zsup2
            }
            else{


                if(i==nbLamesH-1){
                    //printf("\n PB ICI !!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
                    pos[i]=pos[i-1]+pasHLIHLT;
                    pos[i+1]=pos[i]+pasHLIQLT;

                    fprintf(pf6,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m*x[i+61],YHLI_SUP,pos[i]+ZHLI_SUP); //pos-Zsup2
                    fprintf(pf8,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m*x[i+61],YHLI_INF,pos[i]-ZHLI_INF); //pos-Zsup2
                    fprintf(pf,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m2*x[i+62],YQLT_SUP,pos[i+1]+ZQLT_SUP); //pos+Zsup1
                    fprintf(pf3,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m2*x[i+62],YQLT_INF,pos[i+1]-ZQLT_INF); //pos+ZQLT_INF
                }
                else if(i==nbLamesTotal-nbLamesH-1){
                    pos[i]=pos[i-1]+pasQLTQLI;
                    pos[i+1]=pos[i]+pasQLIHLT;
                    fprintf(pf5,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m2*x[i+62],YHLT_SUP,pos[i+1]+ZHLT_SUP); //pos+Zsup1
                    fprintf(pf7,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m2*x[i+62],YHLT_INF,pos[i+1]-ZHLT_INF); //pos+ZHLT_INF
                    fprintf(pf2,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m2*x[i+61],YQLI_SUP,pos[i]+ZQLI_SUP); //pos-Zsup2
                    fprintf(pf4,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m2*x[i+61],YQLI_INF,pos[i]-ZQLI_INF); //pos-Zsup2

                }
                else{
                    pos[i]=pos[i-1]+pasQLTQLI;
                    pos[i+1]=pos[i]+pasQLTQLI;

                    fprintf(pf,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m*x[i+62],YQLT_SUP,pos[i+1]+ZQLT_SUP); //pos+Zsup1
                    fprintf(pf2,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m*x[i+61],YQLI_SUP,pos[i]+ZQLI_SUP); //pos-Zsup2
                    fprintf(pf3,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha2,J-10*m*x[i+62],YQLT_INF,pos[i+1]-ZQLT_INF); //pos+ZQLT_INF
                    fprintf(pf4,"%.20lf 1 0 0 %.20lf %.20lf %.20lf  ",alpha1,J-10*m*x[i+61],YQLI_INF,pos[i]-ZQLI_INF); //pos-Zsup2

                }
            }

        }





        //printf("\ncompute valuesMLC.dat for second Bank...ok\n");
        fclose(pf);
        fclose(pf2);
        fclose(pf3);
        fclose(pf4);
        fclose(pf5);
        fclose(pf6);
        fclose(pf7);
        fclose(pf8);



        failure=0;

    return failure;
}
